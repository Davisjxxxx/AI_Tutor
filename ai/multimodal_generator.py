#!/usr/bin/env python3
"""
Advanced Multi-Modal Content Generator
Generates videos, audio, images, and interactive content using cutting-edge AI
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import base64
import tempfile
from pathlib import Path

# AI and media processing imports
try:
    import openai
    from elevenlabs import generate, Voice, VoiceSettings
    import requests
    from PIL import Image, ImageDraw, ImageFont
    import cv2
    import numpy as np
    from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
except ImportError as e:
    logging.warning(f"Some multimodal dependencies not available: {e}")

from ai.next_gen_providers import ai_orchestrator, AIRequest, ContentType

logger = logging.getLogger(__name__)


class MediaType(Enum):
    """Types of media content"""
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    THUMBNAIL = "thumbnail"
    SUBTITLE = "subtitle"
    ANIMATION = "animation"


class VideoStyle(Enum):
    """Video generation styles"""
    TALKING_HEAD = "talking_head"
    SCREEN_RECORDING = "screen_recording"
    ANIMATION = "animation"
    SLIDESHOW = "slideshow"
    SPLIT_SCREEN = "split_screen"
    CINEMATIC = "cinematic"
    DOCUMENTARY = "documentary"


class VoiceType(Enum):
    """Voice types for audio generation"""
    PROFESSIONAL_MALE = "professional_male"
    PROFESSIONAL_FEMALE = "professional_female"
    ENERGETIC_YOUNG = "energetic_young"
    AUTHORITATIVE = "authoritative"
    FRIENDLY_CASUAL = "friendly_casual"
    NARRATOR = "narrator"


@dataclass
class MediaGenerationRequest:
    """Request for multi-modal content generation"""
    script: str
    media_types: List[MediaType]
    platform: str
    duration_seconds: int = 30
    
    # Video specifications
    video_style: VideoStyle = VideoStyle.TALKING_HEAD
    resolution: str = "1080x1920"  # Vertical for social media
    fps: int = 30
    
    # Audio specifications
    voice_type: VoiceType = VoiceType.PROFESSIONAL_FEMALE
    background_music: bool = True
    sound_effects: bool = True
    
    # Visual specifications
    brand_colors: List[str] = None
    logo_url: str = ""
    visual_theme: str = "modern"
    
    # Content specifications
    include_subtitles: bool = True
    include_thumbnails: bool = True
    thumbnail_count: int = 3


@dataclass
class GeneratedMedia:
    """Generated media content"""
    media_type: MediaType
    file_path: str
    file_url: str
    metadata: Dict[str, Any]
    generation_time: float
    file_size_mb: float


@dataclass
class MultiModalOutput:
    """Complete multi-modal content package"""
    request_id: str
    generated_media: List[GeneratedMedia]
    total_generation_time: float
    estimated_performance: Dict[str, Any]
    optimization_suggestions: List[str]


class AIVideoGenerator:
    """Generates AI videos using various techniques"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.video_templates = self._load_video_templates()
    
    def _load_video_templates(self) -> Dict[VideoStyle, Dict[str, Any]]:
        """Load video generation templates"""
        return {
            VideoStyle.TALKING_HEAD: {
                "avatar_style": "professional",
                "background": "office",
                "camera_angle": "medium_shot",
                "lighting": "soft_professional"
            },
            VideoStyle.ANIMATION: {
                "style": "2d_motion_graphics",
                "transitions": "smooth_fade",
                "text_animations": "typewriter",
                "color_scheme": "vibrant"
            },
            VideoStyle.SLIDESHOW: {
                "slide_duration": 3,
                "transition_type": "slide",
                "text_overlay": True,
                "background_music": True
            }
        }
    
    async def generate_video(self, script: str, style: VideoStyle, 
                           duration: int, resolution: str) -> GeneratedMedia:
        """Generate video content"""
        start_time = datetime.now()
        
        try:
            if style == VideoStyle.TALKING_HEAD:
                video_path = await self._generate_talking_head_video(script, duration, resolution)
            elif style == VideoStyle.ANIMATION:
                video_path = await self._generate_animated_video(script, duration, resolution)
            elif style == VideoStyle.SLIDESHOW:
                video_path = await self._generate_slideshow_video(script, duration, resolution)
            else:
                # Default to slideshow
                video_path = await self._generate_slideshow_video(script, duration, resolution)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            
            return GeneratedMedia(
                media_type=MediaType.VIDEO,
                file_path=str(video_path),
                file_url=f"/media/videos/{Path(video_path).name}",
                metadata={
                    "style": style.value,
                    "duration": duration,
                    "resolution": resolution,
                    "fps": 30
                },
                generation_time=generation_time,
                file_size_mb=file_size
            )
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            raise
    
    async def _generate_talking_head_video(self, script: str, duration: int, resolution: str) -> str:
        """Generate talking head style video"""
        # For now, create a simple video with text overlay
        # In production, this would use AI avatar generation services
        
        width, height = map(int, resolution.split('x'))
        
        # Create background
        background = np.zeros((height, width, 3), dtype=np.uint8)
        background[:] = (30, 30, 30)  # Dark background
        
        # Add text overlay
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        color = (255, 255, 255)
        thickness = 2
        
        # Split script into lines
        words = script.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) < 40:  # Approximate character limit per line
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Create video frames
        fps = 30
        total_frames = duration * fps
        frames = []
        
        for frame_num in range(total_frames):
            frame = background.copy()
            
            # Calculate which lines to show based on frame
            lines_per_second = len(lines) / duration
            current_line_index = int(frame_num / fps * lines_per_second)
            
            # Show current and next few lines
            y_offset = height // 2 - 50
            for i in range(min(3, len(lines) - current_line_index)):
                if current_line_index + i < len(lines):
                    line = lines[current_line_index + i]
                    text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
                    x = (width - text_size[0]) // 2
                    y = y_offset + i * 60
                    
                    cv2.putText(frame, line, (x, y), font, font_scale, color, thickness)
            
            frames.append(frame)
        
        # Save video
        output_path = self.temp_dir / f"talking_head_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        return str(output_path)
    
    async def _generate_animated_video(self, script: str, duration: int, resolution: str) -> str:
        """Generate animated video"""
        # Simplified animation - in production would use advanced animation libraries
        return await self._generate_slideshow_video(script, duration, resolution)
    
    async def _generate_slideshow_video(self, script: str, duration: int, resolution: str) -> str:
        """Generate slideshow-style video"""
        width, height = map(int, resolution.split('x'))
        
        # Create slides from script
        sentences = script.split('.')
        slides = [s.strip() for s in sentences if s.strip()]
        
        if not slides:
            slides = [script]
        
        # Create video frames
        fps = 30
        frames_per_slide = (duration * fps) // len(slides)
        frames = []
        
        colors = [
            (64, 128, 255),   # Blue
            (255, 64, 128),   # Pink
            (128, 255, 64),   # Green
            (255, 128, 64),   # Orange
        ]
        
        for slide_idx, slide_text in enumerate(slides):
            color = colors[slide_idx % len(colors)]
            
            for frame_num in range(frames_per_slide):
                # Create gradient background
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                
                # Simple gradient
                for y in range(height):
                    intensity = y / height
                    frame[y, :] = [int(c * intensity) for c in color]
                
                # Add text
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.2
                text_color = (255, 255, 255)
                thickness = 2
                
                # Word wrap
                words = slide_text.split()
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
                    if text_size[0] < width - 100:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                
                # Center text vertically
                total_text_height = len(lines) * 50
                start_y = (height - total_text_height) // 2
                
                for line_idx, line in enumerate(lines):
                    text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
                    x = (width - text_size[0]) // 2
                    y = start_y + line_idx * 50
                    
                    cv2.putText(frame, line, (x, y), font, font_scale, text_color, thickness)
                
                frames.append(frame)
        
        # Save video
        output_path = self.temp_dir / f"slideshow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        return str(output_path)


class AIAudioGenerator:
    """Generates AI audio using ElevenLabs and other services"""
    
    def __init__(self):
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_mapping = self._get_voice_mapping()
    
    def _get_voice_mapping(self) -> Dict[VoiceType, str]:
        """Map voice types to ElevenLabs voice IDs"""
        return {
            VoiceType.PROFESSIONAL_FEMALE: "EXAVITQu4vr4xnSDxMaL",  # Bella
            VoiceType.PROFESSIONAL_MALE: "VR6AewLTigWG4xSOukaG",    # Arnold
            VoiceType.ENERGETIC_YOUNG: "pNInz6obpgDQGcFmaJgB",      # Adam
            VoiceType.AUTHORITATIVE: "Yko7PKHZNXotIFUBG7I9",       # Antoni
            VoiceType.FRIENDLY_CASUAL: "TxGEqnHWrfWFTfGW9XjX",     # Josh
            VoiceType.NARRATOR: "onwK4e9ZLuTAKqWW03F9"              # Daniel
        }
    
    async def generate_audio(self, script: str, voice_type: VoiceType, 
                           include_music: bool = True) -> GeneratedMedia:
        """Generate audio from script"""
        start_time = datetime.now()
        
        try:
            # Generate speech
            if self.elevenlabs_api_key:
                audio_path = await self._generate_elevenlabs_audio(script, voice_type)
            else:
                # Fallback to OpenAI TTS
                audio_path = await self._generate_openai_audio(script)
            
            # Add background music if requested
            if include_music:
                audio_path = await self._add_background_music(audio_path)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            file_size = os.path.getsize(audio_path) / (1024 * 1024)  # MB
            
            return GeneratedMedia(
                media_type=MediaType.AUDIO,
                file_path=str(audio_path),
                file_url=f"/media/audio/{Path(audio_path).name}",
                metadata={
                    "voice_type": voice_type.value,
                    "duration": await self._get_audio_duration(audio_path),
                    "sample_rate": 44100,
                    "format": "mp3"
                },
                generation_time=generation_time,
                file_size_mb=file_size
            )
            
        except Exception as e:
            logger.error(f"Audio generation failed: {e}")
            raise
    
    async def _generate_elevenlabs_audio(self, script: str, voice_type: VoiceType) -> str:
        """Generate audio using ElevenLabs"""
        voice_id = self.voice_mapping.get(voice_type, self.voice_mapping[VoiceType.PROFESSIONAL_FEMALE])
        
        audio = generate(
            text=script,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5)
            )
        )
        
        output_path = Path(tempfile.mkdtemp()) / f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        
        with open(output_path, 'wb') as f:
            f.write(audio)
        
        return str(output_path)
    
    async def _generate_openai_audio(self, script: str) -> str:
        """Generate audio using OpenAI TTS as fallback"""
        client = openai.AsyncOpenAI()
        
        response = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=script
        )
        
        output_path = Path(tempfile.mkdtemp()) / f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return str(output_path)
    
    async def _add_background_music(self, audio_path: str) -> str:
        """Add background music to audio"""
        # Simplified - in production would use proper audio mixing
        return audio_path
    
    async def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            audio.close()
            return duration
        except:
            return 0.0


class MultiModalContentGenerator:
    """Main class for generating multi-modal content"""
    
    def __init__(self):
        self.video_generator = AIVideoGenerator()
        self.audio_generator = AIAudioGenerator()
        self.generation_queue = asyncio.Queue()
    
    async def generate_content_package(self, request: MediaGenerationRequest) -> MultiModalOutput:
        """Generate complete multi-modal content package"""
        start_time = datetime.now()
        generated_media = []
        
        logger.info(f"Starting multi-modal generation for {len(request.media_types)} media types")
        
        # Generate each requested media type
        generation_tasks = []
        
        if MediaType.VIDEO in request.media_types:
            task = self._generate_video_content(request)
            generation_tasks.append(task)
        
        if MediaType.AUDIO in request.media_types:
            task = self._generate_audio_content(request)
            generation_tasks.append(task)
        
        if MediaType.IMAGE in request.media_types:
            task = self._generate_image_content(request)
            generation_tasks.append(task)
        
        if MediaType.THUMBNAIL in request.media_types:
            task = self._generate_thumbnail_content(request)
            generation_tasks.append(task)
        
        # Execute all generation tasks
        results = await asyncio.gather(*generation_tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, GeneratedMedia):
                generated_media.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Media generation failed: {result}")
        
        total_time = (datetime.now() - start_time).total_seconds()
        
        # Generate performance estimates
        performance_estimate = await self._estimate_performance(generated_media, request)
        
        # Generate optimization suggestions
        optimization_suggestions = await self._generate_optimization_suggestions(generated_media, request)
        
        return MultiModalOutput(
            request_id=f"mm_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            generated_media=generated_media,
            total_generation_time=total_time,
            estimated_performance=performance_estimate,
            optimization_suggestions=optimization_suggestions
        )
    
    async def _generate_video_content(self, request: MediaGenerationRequest) -> GeneratedMedia:
        """Generate video content"""
        return await self.video_generator.generate_video(
            request.script,
            request.video_style,
            request.duration_seconds,
            request.resolution
        )
    
    async def _generate_audio_content(self, request: MediaGenerationRequest) -> GeneratedMedia:
        """Generate audio content"""
        return await self.audio_generator.generate_audio(
            request.script,
            request.voice_type,
            request.background_music
        )
    
    async def _generate_image_content(self, request: MediaGenerationRequest) -> GeneratedMedia:
        """Generate image content"""
        # Placeholder for image generation
        # In production, would use DALL-E, Midjourney, or Stable Diffusion
        start_time = datetime.now()
        
        # Create simple placeholder image
        width, height = 1080, 1080
        image = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(image)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        text = "AI Generated Content"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        output_path = Path(tempfile.mkdtemp()) / f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(output_path)
        
        generation_time = (datetime.now() - start_time).total_seconds()
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        
        return GeneratedMedia(
            media_type=MediaType.IMAGE,
            file_path=str(output_path),
            file_url=f"/media/images/{output_path.name}",
            metadata={"width": width, "height": height, "format": "PNG"},
            generation_time=generation_time,
            file_size_mb=file_size
        )
    
    async def _generate_thumbnail_content(self, request: MediaGenerationRequest) -> GeneratedMedia:
        """Generate thumbnail content"""
        # Similar to image generation but optimized for thumbnails
        return await self._generate_image_content(request)
    
    async def _estimate_performance(self, media: List[GeneratedMedia], 
                                  request: MediaGenerationRequest) -> Dict[str, Any]:
        """Estimate content performance"""
        return {
            "estimated_views": 10000,
            "estimated_engagement_rate": 0.08,
            "estimated_shares": 500,
            "viral_potential": 0.7
        }
    
    async def _generate_optimization_suggestions(self, media: List[GeneratedMedia],
                                               request: MediaGenerationRequest) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = [
            "Add captions for better accessibility",
            "Include trending hashtags",
            "Optimize thumbnail for click-through rate",
            "Consider A/B testing different hooks"
        ]
        
        return suggestions


# Global multimodal generator instance
multimodal_generator = MultiModalContentGenerator()
