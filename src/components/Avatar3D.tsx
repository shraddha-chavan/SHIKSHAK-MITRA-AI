import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Sphere, Box, Cylinder } from '@react-three/drei';
import { motion } from 'framer-motion';
import * as THREE from 'three';

// Emotion types
type Emotion = 'happy' | 'sad' | 'excited' | 'thinking' | 'speaking' | 'listening' | 'confused' | 'neutral';

interface Avatar3DProps {
  emotion: Emotion;
  isListening: boolean;
  isSpeaking: boolean;
  message?: string;
}

// 3D Avatar Head Component
const AvatarHead: React.FC<{ emotion: Emotion; isSpeaking: boolean; isListening: boolean }> = ({ 
  emotion, 
  isSpeaking, 
  isListening 
}) => {
  const headRef = useRef<THREE.Mesh>(null);
  const leftEyeRef = useRef<THREE.Mesh>(null);
  const rightEyeRef = useRef<THREE.Mesh>(null);
  const mouthRef = useRef<THREE.Mesh>(null);

  // Animation loop
  useFrame((state) => {
    if (headRef.current) {
      // Gentle head bobbing
      headRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
      headRef.current.position.y = Math.sin(state.clock.elapsedTime * 2) * 0.05;
    }

    // Eye blinking animation
    if (leftEyeRef.current && rightEyeRef.current) {
      const blinkTime = Math.sin(state.clock.elapsedTime * 3);
      if (blinkTime > 0.95) {
        leftEyeRef.current.scale.y = 0.1;
        rightEyeRef.current.scale.y = 0.1;
      } else {
        leftEyeRef.current.scale.y = 1;
        rightEyeRef.current.scale.y = 1;
      }
    }

    // Mouth animation for speaking
    if (mouthRef.current && isSpeaking) {
      mouthRef.current.scale.x = 1 + Math.sin(state.clock.elapsedTime * 8) * 0.3;
      mouthRef.current.scale.y = 1 + Math.sin(state.clock.elapsedTime * 6) * 0.2;
    }
  });

  // Get colors based on emotion
  const getEmotionColors = (emotion: Emotion) => {
    switch (emotion) {
      case 'happy': return { head: '#FFE4B5', cheeks: '#FFB6C1' };
      case 'sad': return { head: '#E6E6FA', cheeks: '#B0C4DE' };
      case 'excited': return { head: '#FFF8DC', cheeks: '#FF69B4' };
      case 'thinking': return { head: '#F0F8FF', cheeks: '#DDA0DD' };
      case 'speaking': return { head: '#FFFACD', cheeks: '#98FB98' };
      case 'listening': return { head: '#F5FFFA', cheeks: '#87CEEB' };
      case 'confused': return { head: '#FDF5E6', cheeks: '#F0E68C' };
      default: return { head: '#FFEFD5', cheeks: '#FFDAB9' };
    }
  };

  const colors = getEmotionColors(emotion);

  return (
    <group ref={headRef}>
      {/* Head */}
      <Sphere args={[1, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial color={colors.head} />
      </Sphere>

      {/* Eyes */}
      <Sphere ref={leftEyeRef} args={[0.15, 16, 16]} position={[-0.3, 0.2, 0.8]}>
        <meshStandardMaterial color="#000" />
      </Sphere>
      <Sphere ref={rightEyeRef} args={[0.15, 16, 16]} position={[0.3, 0.2, 0.8]}>
        <meshStandardMaterial color="#000" />
      </Sphere>

      {/* Eyebrows */}
      <Box args={[0.4, 0.05, 0.1]} position={[-0.3, 0.4, 0.8]} rotation={[0, 0, emotion === 'confused' ? 0.3 : 0]}>
        <meshStandardMaterial color="#8B4513" />
      </Box>
      <Box args={[0.4, 0.05, 0.1]} position={[0.3, 0.4, 0.8]} rotation={[0, 0, emotion === 'confused' ? -0.3 : 0]}>
        <meshStandardMaterial color="#8B4513" />
      </Box>

      {/* Nose */}
      <Cylinder args={[0.05, 0.08, 0.3]} position={[0, 0, 0.9]} rotation={[Math.PI / 2, 0, 0]}>
        <meshStandardMaterial color={colors.head} />
      </Cylinder>

      {/* Mouth */}
      <Sphere 
        ref={mouthRef} 
        args={[0.2, 16, 8]} 
        position={[0, -0.3, 0.8]}
        scale={[
          emotion === 'happy' ? 1.5 : emotion === 'sad' ? 0.8 : 1,
          emotion === 'happy' ? 0.5 : emotion === 'sad' ? 1.2 : 1,
          1
        ]}
      >
        <meshStandardMaterial color="#FF6B6B" />
      </Sphere>

      {/* Cheeks (for emotions) */}
      {(emotion === 'happy' || emotion === 'excited') && (
        <>
          <Sphere args={[0.1, 16, 16]} position={[-0.6, -0.1, 0.6]}>
            <meshStandardMaterial color={colors.cheeks} />
          </Sphere>
          <Sphere args={[0.1, 16, 16]} position={[0.6, -0.1, 0.6]}>
            <meshStandardMaterial color={colors.cheeks} />
          </Sphere>
        </>
      )}

      {/* Listening indicator */}
      {isListening && (
        <group position={[1.5, 0.5, 0]}>
          <Sphere args={[0.1, 8, 8]}>
            <meshStandardMaterial color="#00FF00" emissive="#00FF00" emissiveIntensity={0.5} />
          </Sphere>
          <Text fontSize={0.2} color="#00FF00" position={[0, -0.3, 0]}>
            Listening...
          </Text>
        </group>
      )}

      {/* Speaking indicator */}
      {isSpeaking && (
        <group position={[-1.5, 0.5, 0]}>
          <Sphere args={[0.1, 8, 8]}>
            <meshStandardMaterial color="#FF4500" emissive="#FF4500" emissiveIntensity={0.5} />
          </Sphere>
          <Text fontSize={0.2} color="#FF4500" position={[0, -0.3, 0]}>
            Speaking...
          </Text>
        </group>
      )}
    </group>
  );
};

// Floating particles for emotion effects
const EmotionParticles: React.FC<{ emotion: Emotion }> = ({ emotion }) => {
  const particlesRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.01;
    }
  });

  const getParticleColor = (emotion: Emotion) => {
    switch (emotion) {
      case 'happy': return '#FFD700';
      case 'excited': return '#FF69B4';
      case 'thinking': return '#9370DB';
      case 'speaking': return '#32CD32';
      case 'listening': return '#00CED1';
      default: return '#87CEEB';
    }
  };

  return (
    <group ref={particlesRef}>
      {Array.from({ length: 8 }).map((_, i) => (
        <Sphere
          key={i}
          args={[0.02, 8, 8]}
          position={[
            Math.cos((i / 8) * Math.PI * 2) * 2,
            Math.sin((i / 8) * Math.PI * 2) * 0.5,
            Math.sin((i / 8) * Math.PI * 2) * 2
          ]}
        >
          <meshStandardMaterial 
            color={getParticleColor(emotion)} 
            emissive={getParticleColor(emotion)} 
            emissiveIntensity={0.3} 
          />
        </Sphere>
      ))}
    </group>
  );
};

// Main Avatar3D Component
const Avatar3D: React.FC<Avatar3DProps> = ({ emotion, isListening, isSpeaking, message }) => {
  return (
    <div className="relative w-full h-full">
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        {/* Lighting */}
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#4A90E2" />

        {/* Avatar */}
        <AvatarHead emotion={emotion} isSpeaking={isSpeaking} isListening={isListening} />
        
        {/* Emotion particles */}
        <EmotionParticles emotion={emotion} />

        {/* Controls */}
        <OrbitControls enableZoom={false} enablePan={false} />
      </Canvas>

      {/* Message overlay */}
      {message && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="absolute bottom-4 left-4 right-4 bg-black/80 text-white p-3 rounded-lg backdrop-blur-sm"
        >
          <p className="text-sm">{message}</p>
        </motion.div>
      )}

      {/* Emotion indicator */}
      <div className="absolute top-4 right-4 bg-white/90 px-3 py-1 rounded-full text-sm font-medium capitalize">
        {emotion}
      </div>
    </div>
  );
};

export default Avatar3D;