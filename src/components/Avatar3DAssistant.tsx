import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Sphere, Box, Torus } from '@react-three/drei';
import * as THREE from 'three';

interface Avatar3DAssistantProps {
  isActive: boolean;
  isSpeaking: boolean;
  message?: string;
}

// Holographic AI Core
const AICore: React.FC<{ isActive: boolean; isSpeaking: boolean }> = ({ isActive, isSpeaking }) => {
  const coreRef = useRef<THREE.Group>(null);
  const ringsRef = useRef<THREE.Group>(null);
  const particlesRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (coreRef.current) {
      coreRef.current.rotation.y += 0.01;
      coreRef.current.position.y = Math.sin(state.clock.elapsedTime * 2) * 0.1;
    }
    
    if (ringsRef.current) {
      ringsRef.current.rotation.x += 0.005;
      ringsRef.current.rotation.z += 0.008;
    }

    if (particlesRef.current && isActive) {
      particlesRef.current.rotation.y += 0.02;
    }
  });

  return (
    <group>
      {/* Central AI Core */}
      <group ref={coreRef}>
        <Sphere args={[0.3, 32, 32]}>
          <meshStandardMaterial 
            color={isActive ? "#00FFFF" : "#666666"} 
            emissive={isActive ? "#0088FF" : "#333333"}
            emissiveIntensity={isSpeaking ? 0.8 : 0.3}
            transparent
            opacity={0.8}
          />
        </Sphere>
        
        {/* Inner energy core */}
        <Sphere args={[0.15, 16, 16]}>
          <meshStandardMaterial 
            color="#FFFFFF" 
            emissive="#FFFFFF"
            emissiveIntensity={isSpeaking ? 1.2 : 0.6}
          />
        </Sphere>
      </group>

      {/* Rotating energy rings */}
      <group ref={ringsRef}>
        <Torus args={[0.6, 0.02, 8, 32]}>
          <meshStandardMaterial 
            color={isActive ? "#00FFAA" : "#444444"}
            emissive={isActive ? "#00FFAA" : "#222222"}
            emissiveIntensity={0.5}
          />
        </Torus>
        <Torus args={[0.8, 0.015, 8, 32]} rotation={[Math.PI / 2, 0, 0]}>
          <meshStandardMaterial 
            color={isActive ? "#FF00AA" : "#444444"}
            emissive={isActive ? "#FF00AA" : "#222222"}
            emissiveIntensity={0.4}
          />
        </Torus>
        <Torus args={[0.7, 0.01, 8, 32]} rotation={[0, Math.PI / 4, Math.PI / 3]}>
          <meshStandardMaterial 
            color={isActive ? "#AAFF00" : "#444444"}
            emissive={isActive ? "#AAFF00" : "#222222"}
            emissiveIntensity={0.3}
          />
        </Torus>
      </group>

      {/* Floating data particles */}
      {isActive && (
        <group ref={particlesRef}>
          {Array.from({ length: 12 }).map((_, i) => (
            <Sphere
              key={i}
              args={[0.02, 8, 8]}
              position={[
                Math.cos((i / 12) * Math.PI * 2) * 1.2,
                Math.sin((i / 6) * Math.PI) * 0.3,
                Math.sin((i / 12) * Math.PI * 2) * 1.2
              ]}
            >
              <meshStandardMaterial 
                color="#00FFFF"
                emissive="#00FFFF"
                emissiveIntensity={0.8}
              />
            </Sphere>
          ))}
        </group>
      )}

      {/* Holographic face projection */}
      {isActive && (
        <group position={[0, 0, 0.4]}>
          {/* Eyes */}
          <Sphere args={[0.05, 8, 8]} position={[-0.1, 0.1, 0]}>
            <meshStandardMaterial color="#00FFFF" emissive="#00FFFF" emissiveIntensity={1} />
          </Sphere>
          <Sphere args={[0.05, 8, 8]} position={[0.1, 0.1, 0]}>
            <meshStandardMaterial color="#00FFFF" emissive="#00FFFF" emissiveIntensity={1} />
          </Sphere>
          
          {/* Mouth indicator */}
          {isSpeaking && (
            <Box args={[0.15, 0.03, 0.02]} position={[0, -0.05, 0]}>
              <meshStandardMaterial 
                color="#FF4400" 
                emissive="#FF4400" 
                emissiveIntensity={0.8}
              />
            </Box>
          )}
        </group>
      )}
    </group>
  );
};

// Main 3D Avatar Component
const Avatar3DAssistant: React.FC<Avatar3DAssistantProps> = ({ isActive, isSpeaking, message }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(isActive);
  }, [isActive]);

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-20 right-6 w-64 h-64 z-40 pointer-events-none">
      <div className="relative w-full h-full bg-black/20 rounded-full backdrop-blur-sm border border-cyan-500/30">
        <Canvas camera={{ position: [0, 0, 3], fov: 50 }}>
          {/* Lighting setup */}
          <ambientLight intensity={0.2} />
          <pointLight position={[2, 2, 2]} intensity={1} color="#00FFFF" />
          <pointLight position={[-2, -2, -2]} intensity={0.5} color="#FF00AA" />
          
          {/* AI Assistant */}
          <AICore isActive={isActive} isSpeaking={isSpeaking} />
          
          {/* Auto-rotate camera */}
          <OrbitControls 
            enableZoom={false} 
            enablePan={false} 
            autoRotate={isActive}
            autoRotateSpeed={0.5}
          />
        </Canvas>

        {/* Status indicators */}
        <div className="absolute top-2 left-2 text-xs text-cyan-400 font-mono">
          {isActive ? 'ONLINE' : 'OFFLINE'}
        </div>
        
        {isSpeaking && (
          <div className="absolute top-2 right-2 text-xs text-orange-400 font-mono animate-pulse">
            TRANSMITTING
          </div>
        )}

        {/* Message display */}
        {message && (
          <div className="absolute -top-16 left-0 right-0 bg-black/80 text-cyan-300 text-sm p-2 rounded-lg border border-cyan-500/50">
            <div className="font-mono">{message}</div>
          </div>
        )}

        {/* Holographic scan lines */}
        {isActive && (
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-500/10 to-transparent animate-pulse"></div>
            <div className="absolute top-0 left-0 right-0 h-px bg-cyan-400/50 animate-ping"></div>
            <div className="absolute bottom-0 left-0 right-0 h-px bg-cyan-400/50 animate-ping" style={{animationDelay: '1s'}}></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Avatar3DAssistant;