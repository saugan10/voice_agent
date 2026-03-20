#!/usr/bin/env python3
"""Simple Gemini voice bot example with Mem0 memory.

Demonstrates using:
- Deepgram STT
- Gemini LLM
- Cartesia TTS
- Mem0 memory service (optional, if MEM0_API_KEY is set)
"""

import os
import sys

from dotenv import load_dotenv
from loguru import logger

from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport

from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.google.llm import GoogleLLMService
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.transports.base_transport import BaseTransport

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3
from pipecat.audio.turn.smart_turn.base_smart_turn import SmartTurnParams

from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
)
from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor

# 🔁 NEW: Mem0 memory integration
from pipecat.services.mem0.memory import Mem0MemoryService

load_dotenv(override=True)

# ---------------------------------------------------------------------------
# CLI parsing for custom STT flag (unchanged)
# ---------------------------------------------------------------------------

# Pre-parse a custom --stt CLI flag so the pipecat runner's argparser
# (which is invoked later) doesn't reject it. Supported choices:
# google|dummy|manual|local|deepgram
STT_CHOICE = None
for i, a in enumerate(list(sys.argv)):
    if a.startswith("--stt="):
        STT_CHOICE = a.split("=", 1)[1]
        # remove this arg so downstream parsers don't see it
        sys.argv.pop(i)
        break
    if a == "--stt":
        try:
            STT_CHOICE = sys.argv[i + 1]
            # remove both entries
            sys.argv.pop(i)
            sys.argv.pop(i)
        except Exception:
            # missing value — leave as None and let later code handle it
            STT_CHOICE = None
        break


def _daily_params_factory():
    try:
        from pipecat.transports.daily.transport import DailyParams
    except Exception as e:
        logger.warning(
            "Daily transport not available. Falling back to WebRTC transport. "
            "To use Daily, install 'daily-python'."
        )
        return _webrtc_params_factory()

    return DailyParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
        turn_analyzer=LocalSmartTurnAnalyzerV3(params=SmartTurnParams()),
    )


def _fastapi_ws_params_factory():
    try:
        from pipecat.transports.websocket.fastapi import FastAPIWebsocketParams
    except Exception as e:
        raise Exception(
            "FastAPI Websocket transport not available. Install required extras "
            "or use another transport."
        ) from e

    return FastAPIWebsocketParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
        turn_analyzer=LocalSmartTurnAnalyzerV3(params=SmartTurnParams()),
    )


def _webrtc_params_factory():
    try:
        from pipecat.transports.base_transport import TransportParams
    except Exception as e:
        raise Exception(
            "WebRTC transport not available. Install required extras or use "
            "another transport."
        ) from e

    return TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
        turn_analyzer=LocalSmartTurnAnalyzerV3(params=SmartTurnParams()),
    )


transport_params = {
    "daily": lambda: _daily_params_factory(),
    "twilio": lambda: _fastapi_ws_params_factory(),
    "webrtc": lambda: _webrtc_params_factory(),
}


# ---------------------------------------------------------------------------
# Main bot
# ---------------------------------------------------------------------------

async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    logger.info("Starting Gemini voice bot with Mem0 (if configured)")

    USER_ID = "gemini-mem0-user"  # you can swap to a real user id per caller

    # STT using Deepgram (uses `DEEPGRAM_API_KEY` env var).
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    if not deepgram_api_key:
        logger.warning("DEEPGRAM_API_KEY not set — Deepgram STT may not work.")

    stt = DeepgramSTTService(api_key=deepgram_api_key)

    # Log STT transcripts as they arrive for debugging
    try:
        @stt.on_transcript()
        async def _on_transcript(transcript, is_final: bool = True):
            logger.info(
                f"STT transcript{' (final)' if is_final else ''}: {transcript}"
            )
    except Exception:
        # Not all STT services expose the same decorator API; ignore if unavailable
        pass

    # LLM using Gemini (api key)
    llm = GoogleLLMService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash",
    )

    # Log assistant messages from the LLM for debugging
    try:
        @llm.on_assistant_response()
        async def _on_assistant_response(response_text: str):
            logger.info(f"LLM assistant response: {response_text}")
    except Exception:
        # Fallback: some adapters may not provide this hook
        pass

    # TTS using Cartesia (simple API key from env)
    cartesia_api_key = os.getenv("CARTESIA_API_KEY")
    if not cartesia_api_key:
        logger.warning("CARTESIA_API_KEY not set — TTS may not work.")

    tts = CartesiaTTSService(
        api_key=cartesia_api_key,
        voice_id="71a7ad14-091c-4e8e-a314-022ece01c121",  # British Reading Lady
    )

    # Conversation system prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful voice assistant. "
                "Keep responses short, speak naturally, and use any relevant memories "
                "about the user that are provided to you."
            ),
        }
    ]

    context = LLMContext(messages)
    context_aggregator = LLMContextAggregatorPair(context)

    # 🔁 Mem0 memory service (optional – only if MEM0_API_KEY is set)
    mem0_api_key = os.getenv("MEM0_API_KEY")
    memory = None
    if not mem0_api_key:
        logger.warning(
            "MEM0_API_KEY not set — Mem0 memory will be disabled. "
            "Set it in your .env to enable persistent memory."
        )
    else:
        logger.info("Mem0 memory enabled.")
        memory = Mem0MemoryService(
            api_key=mem0_api_key,
            user_id=USER_ID,
            agent_id="gemini-voice-agent",
            run_id="session1",
            params=Mem0MemoryService.InputParams(
                search_limit=10,
                search_threshold=0.3,
                api_version="v2",
                system_prompt=(
                    "Here are some things I remember about this user from "
                    "past conversations:\n\n"
                ),
                add_as_system_message=True,
                position=1,  # insert after the main system prompt
            ),
        )

    rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

    # Build pipeline dynamically so it still runs without Mem0
    pipeline_stages = [
        transport.input(),
        rtvi,  # RTVI processor for conversation display
        stt,
        context_aggregator.user(),
    ]

    if memory is not None:
        pipeline_stages.append(memory)  # 🧠 inject Mem0 before LLM

    pipeline_stages.extend(
        [
            llm,
            tts,
            transport.output(),
            context_aggregator.assistant(),
        ]
    )

    pipeline = Pipeline(pipeline_stages)

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        idle_timeout_secs=runner_args.pipeline_idle_timeout_secs,
        observers=[RTVIObserver(rtvi)],
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info(f"🎉 Client connected: {client}")
        logger.info(
            "📞 Starting conversation — queuing initial LLM frame..."
        )

        # Optional: frame observer just for debug
        try:
            inp = transport.input()

            async def _frame_observer(frame):
                try:
                    tname = type(frame).__name__
                except Exception:
                    tname = str(frame)
                logger.debug(f"Received frame: {tname}")

            if hasattr(inp, "add_observer"):
                inp.add_observer(_frame_observer)
                logger.debug("Attached frame observer via add_observer")
            elif hasattr(inp, "register_frame_handler"):
                inp.register_frame_handler(_frame_observer)
                logger.debug("Attached frame observer via register_frame_handler")
        except Exception as e:
            logger.debug(f"Could not attach frame observer: {e}")

        # Kick off the first LLM run; Mem0 (if enabled) will contribute
        await task.queue_frames([LLMRunFrame()])
        logger.info("✅ Initial LLM frame queued — bot is now active!")

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected — cancelling task")
        await task.cancel()

    # Extra logging for transport tracks (unchanged)
    try:
        @transport.event_handler("on_track_started")
        async def _on_track_started(transport, event):
            try:
                p = (
                    event.get("participant")
                    if isinstance(event, dict)
                    else getattr(event, "participant", None)
                )
            except Exception:
                p = None
            logger.info(
                f"Track started event: "
                f"type={event.get('type') if isinstance(event, dict) else getattr(event, 'type', None)} "
                f"participant={p} raw={event}"
            )

        @transport.event_handler("on_track_stopped")
        async def _on_track_stopped(transport, event):
            try:
                p = (
                    event.get("participant")
                    if isinstance(event, dict)
                    else getattr(event, "participant", None)
                )
            except Exception:
                p = None
            logger.info(
                f"Track stopped event: "
                f"type={event.get('type') if isinstance(event, dict) else getattr(event, 'type', None)} "
                f"participant={p} raw={event}"
            )
    except Exception:
        # Not all transports expose these high-level event names — ignore if unavailable.
        pass

    runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)
    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    transport = await create_transport(runner_args, transport_params)
    await run_bot(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
