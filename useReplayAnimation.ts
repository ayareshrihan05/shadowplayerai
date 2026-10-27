import { useEffect, useRef } from 'react';
import { useAppStore } from '../store/appStore';

export function useReplayAnimation(totalFrames: number) {
  const isPlaying = useAppStore((s) => s.replay.isPlaying);
  const currentFrameIndex = useAppStore((s) => s.replay.currentFrameIndex);
  const playbackSpeed = useAppStore((s) => s.replay.playbackSpeed);
  const setCurrentFrameIndex = useAppStore((s) => s.setCurrentFrameIndex);
  const setIsPlaying = useAppStore((s) => s.setIsPlaying);

  const lastTimeRef = useRef<number | null>(null);

  useEffect(() => {
    if (!isPlaying || totalFrames <= 1) {
      lastTimeRef.current = null;
      return;
    }

    let animationFrameId: number;
    // 1 frame per second in the simulation = 1000ms / playbackSpeed
    const frameIntervalMs = 1000 / playbackSpeed;

    const animate = (now: number) => {
      if (lastTimeRef.current === null) {
        lastTimeRef.current = now;
      }

      const elapsed = now - lastTimeRef.current;

      if (elapsed >= frameIntervalMs) {
        const nextIndex = currentFrameIndex + 1;
        if (nextIndex >= totalFrames) {
          setIsPlaying(false);
          lastTimeRef.current = null;
          return;
        } else {
          setCurrentFrameIndex(nextIndex);
          lastTimeRef.current = now;
        }
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [isPlaying, currentFrameIndex, totalFrames, playbackSpeed, setCurrentFrameIndex, setIsPlaying]);
}
