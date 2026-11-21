import React from 'react';

interface IconProps {
  className?: string;
}

/**
 * Multi-tone 16x16 pixel-art SVG sprites with crispEdges rendering (Obsidian 16-bit palette).
 */
export const PixelPythonIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    {/* Upper cyan serpent */}
    <rect x="5" y="2" width="6" height="2" fill="#38BDF8" />
    <rect x="4" y="4" width="7" height="3" fill="#0EA5E9" />
    <rect x="2" y="5" width="4" height="4" fill="#38BDF8" />
    <rect x="6" y="3" width="1" height="1" fill="#F8FAFC" />
    {/* Lower gold serpent */}
    <rect x="5" y="9" width="7" height="3" fill="#F5B942" />
    <rect x="10" y="7" width="4" height="4" fill="#FDE68A" />
    <rect x="5" y="12" width="6" height="2" fill="#D97706" />
    <rect x="9" y="12" width="1" height="1" fill="#0D1017" />
  </svg>
);

export const PixelBoltIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="8" y="1" width="4" height="2" fill="#6EE7B7" />
    <rect x="6" y="3" width="4" height="2" fill="#2DD4A0" />
    <rect x="4" y="5" width="7" height="3" fill="#2DD4A0" />
    <rect x="7" y="8" width="5" height="2" fill="#10B981" />
    <rect x="5" y="10" width="4" height="2" fill="#2DD4A0" />
    <rect x="4" y="12" width="3" height="3" fill="#6EE7B7" />
  </svg>
);

export const PixelSparkIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="7" y="1" width="2" height="4" fill="#C4B5FD" />
    <rect x="7" y="11" width="2" height="4" fill="#A78BFA" />
    <rect x="1" y="7" width="4" height="2" fill="#C4B5FD" />
    <rect x="11" y="7" width="4" height="2" fill="#A78BFA" />
    <rect x="5" y="5" width="6" height="6" fill="#A78BFA" />
    <rect x="7" y="7" width="2" height="2" fill="#F8FAFC" />
  </svg>
);

export const PixelSwordIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="12" y="1" width="3" height="2" fill="#F1F5F9" />
    <rect x="10" y="3" width="3" height="2" fill="#F1F5F9" />
    <rect x="8" y="5" width="3" height="2" fill="#E2E8F0" />
    <rect x="6" y="7" width="3" height="2" fill="#CBD5E1" />
    <rect x="13" y="3" width="1" height="1" fill="#64748B" />
    <rect x="11" y="5" width="1" height="1" fill="#64748B" />
    <rect x="9" y="7" width="1" height="1" fill="#64748B" />
    <rect x="3" y="7" width="2" height="2" fill="#F5B942" />
    <rect x="5" y="9" width="2" height="2" fill="#F5B942" />
    <rect x="7" y="11" width="2" height="2" fill="#C98A1B" />
    <rect x="3" y="10" width="2" height="2" fill="#92400E" />
    <rect x="2" y="11" width="2" height="2" fill="#78350F" />
    <rect x="1" y="13" width="2" height="2" fill="#F45D78" />
  </svg>
);

export const PixelCrownIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="2" y="4" width="2" height="4" fill="#F5B942" />
    <rect x="7" y="2" width="2" height="6" fill="#FDE68A" />
    <rect x="12" y="4" width="2" height="4" fill="#F5B942" />
    <rect x="2" y="7" width="12" height="4" fill="#F5B942" />
    <rect x="2" y="11" width="12" height="2" fill="#C98A1B" />
    <rect x="7" y="8" width="2" height="2" fill="#F45D78" />
    <rect x="3" y="8" width="2" height="2" fill="#38BDF8" />
    <rect x="11" y="8" width="2" height="2" fill="#38BDF8" />
  </svg>
);

export const PixelSkullIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="4" y="2" width="8" height="2" fill="#F1F5F9" />
    <rect x="3" y="4" width="10" height="5" fill="#E2E8F0" />
    <rect x="4" y="9" width="8" height="2" fill="#CBD5E1" />
    <rect x="4" y="5" width="3" height="3" fill="#F45D78" />
    <rect x="5" y="6" width="1" height="1" fill="#FDA4AF" />
    <rect x="9" y="5" width="3" height="3" fill="#F45D78" />
    <rect x="10" y="6" width="1" height="1" fill="#FDA4AF" />
    <rect x="7" y="8" width="2" height="2" fill="#141933" />
    <rect x="4" y="11" width="8" height="3" fill="#94A3B8" />
    <rect x="5" y="11" width="1" height="2" fill="#F1F5F9" />
    <rect x="7" y="11" width="2" height="2" fill="#F1F5F9" />
    <rect x="10" y="11" width="1" height="2" fill="#F1F5F9" />
  </svg>
);

export const PixelCampfireIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="7" y="1" width="2" height="3" fill="#F45D78" />
    <rect x="5" y="3" width="6" height="4" fill="#F97316" />
    <rect x="4" y="6" width="8" height="4" fill="#F97316" />
    <rect x="6" y="4" width="4" height="5" fill="#F5B942" />
    <rect x="7" y="6" width="2" height="3" fill="#FEF08A" />
    <rect x="2" y="11" width="12" height="2" fill="#92400E" />
    <rect x="3" y="13" width="10" height="2" fill="#78350F" />
    <rect x="4" y="10" width="8" height="1" fill="#B45309" />
  </svg>
);

export const PixelScrollIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="3" y="3" width="10" height="10" fill="#FDE68A" />
    <rect x="3" y="11" width="10" height="2" fill="#F5B942" />
    <rect x="2" y="2" width="12" height="2" fill="#C98A1B" />
    <rect x="2" y="12" width="12" height="2" fill="#B45309" />
    <rect x="1" y="2" width="1" height="2" fill="#F5B942" />
    <rect x="14" y="12" width="1" height="2" fill="#F5B942" />
    <rect x="5" y="5" width="6" height="1" fill="#344075" />
    <rect x="5" y="7" width="6" height="1" fill="#344075" />
    <rect x="5" y="9" width="4" height="1" fill="#7C3AED" />
  </svg>
);

export const PixelGateIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="2" y="3" width="12" height="3" fill="#A78BFA" />
    <rect x="4" y="2" width="8" height="2" fill="#C4B5FD" />
    <rect x="2" y="6" width="3" height="8" fill="#7C3AED" />
    <rect x="11" y="6" width="3" height="8" fill="#7C3AED" />
    <rect x="7" y="3" width="2" height="2" fill="#F5B942" />
    <rect x="5" y="6" width="6" height="8" fill="#0B0E1D" />
    <rect x="7" y="8" width="2" height="3" fill="#38BDF8" />
    <rect x="1" y="14" width="14" height="1" fill="#F5B942" />
  </svg>
);

export const PixelFlagIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="3" y="2" width="2" height="13" fill="#CBD5E1" />
    <rect x="3" y="1" width="2" height="1" fill="#F5B942" />
    <rect x="5" y="3" width="8" height="2" fill="#F45D78" />
    <rect x="5" y="5" width="6" height="2" fill="#E11D48" />
    <rect x="5" y="7" width="8" height="2" fill="#F45D78" />
    <rect x="7" y="5" width="2" height="2" fill="#F5B942" />
  </svg>
);

export const PixelCrystalIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="7" y="1" width="2" height="2" fill="#E0F2FE" />
    <rect x="5" y="3" width="6" height="3" fill="#38BDF8" />
    <rect x="4" y="6" width="8" height="4" fill="#22D3EE" />
    <rect x="5" y="10" width="6" height="3" fill="#0284C7" />
    <rect x="7" y="13" width="2" height="2" fill="#0369A1" />
    <rect x="5" y="4" width="2" height="4" fill="#E0F2FE" />
  </svg>
);

export const PixelLeafGemIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="8" y="2" width="5" height="3" fill="#6EE7B7" />
    <rect x="5" y="4" width="8" height="5" fill="#2DD4A0" />
    <rect x="3" y="6" width="6" height="5" fill="#10B981" />
    <rect x="5" y="11" width="5" height="2" fill="#059669" />
    <rect x="6" y="7" width="4" height="2" fill="#D1FAE5" />
    <rect x="2" y="12" width="3" height="2" fill="#059669" />
  </svg>
);

export const PixelTrophyIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="4" y="2" width="8" height="2" fill="#FDE68A" />
    <rect x="2" y="3" width="2" height="4" fill="#C98A1B" />
    <rect x="12" y="3" width="2" height="4" fill="#C98A1B" />
    <rect x="4" y="4" width="8" height="4" fill="#F5B942" />
    <rect x="6" y="8" width="4" height="2" fill="#C98A1B" />
    <rect x="7" y="10" width="2" height="2" fill="#F5B942" />
    <rect x="4" y="12" width="8" height="2" fill="#C98A1B" />
    <rect x="5" y="12" width="6" height="1" fill="#F5B942" />
  </svg>
);

export const PixelMapIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="2" y="3" width="4" height="10" fill="#FDE68A" />
    <rect x="6" y="4" width="4" height="10" fill="#F5B942" />
    <rect x="10" y="2" width="4" height="10" fill="#FDE68A" />
    <rect x="4" y="6" width="2" height="2" fill="#38BDF8" />
    <rect x="7" y="8" width="2" height="2" fill="#A78BFA" />
    <rect x="11" y="5" width="2" height="2" fill="#F45D78" />
  </svg>
);

export const PixelTerminalIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="1" y="2" width="14" height="12" fill="#1C2346" />
    <rect x="2" y="3" width="12" height="10" fill="#0B0E1D" />
    <rect x="4" y="6" width="2" height="1" fill="#F5B942" />
    <rect x="6" y="7" width="2" height="2" fill="#F5B942" />
    <rect x="4" y="9" width="2" height="1" fill="#F5B942" />
    <rect x="8" y="9" width="4" height="2" fill="#2DD4A0" />
  </svg>
);

export const PixelPotionIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="6" y="1" width="4" height="2" fill="#C98A1B" />
    <rect x="7" y="3" width="2" height="3" fill="#CBD5E1" />
    <rect x="5" y="6" width="6" height="2" fill="#A78BFA" />
    <rect x="3" y="8" width="10" height="5" fill="#7C3AED" />
    <rect x="5" y="13" width="6" height="2" fill="#5B21B6" />
    <rect x="5" y="9" width="2" height="3" fill="#E9D5FF" />
  </svg>
);

export const PixelBotIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="7" y="1" width="2" height="2" fill="#F5B942" />
    <rect x="3" y="3" width="10" height="10" fill="#38BDF8" />
    <rect x="4" y="4" width="8" height="8" fill="#141933" />
    <rect x="5" y="6" width="2" height="2" fill="#22D3EE" />
    <rect x="9" y="6" width="2" height="2" fill="#22D3EE" />
    <rect x="5" y="10" width="6" height="1" fill="#2DD4A0" />
  </svg>
);

export const PixelCheckIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="12" y="3" width="2" height="2" fill="#6EE7B7" />
    <rect x="10" y="5" width="2" height="2" fill="#2DD4A0" />
    <rect x="8" y="7" width="2" height="2" fill="#2DD4A0" />
    <rect x="6" y="9" width="2" height="2" fill="#10B981" />
    <rect x="4" y="7" width="2" height="2" fill="#2DD4A0" />
    <rect x="2" y="5" width="2" height="2" fill="#6EE7B7" />
  </svg>
);

export const PixelCrossIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="3" y="3" width="2" height="2" fill="#FDA4AF" />
    <rect x="11" y="3" width="2" height="2" fill="#FDA4AF" />
    <rect x="5" y="5" width="2" height="2" fill="#F45D78" />
    <rect x="9" y="5" width="2" height="2" fill="#F45D78" />
    <rect x="7" y="7" width="2" height="2" fill="#E11D48" />
    <rect x="5" y="9" width="2" height="2" fill="#F45D78" />
    <rect x="9" y="9" width="2" height="2" fill="#F45D78" />
    <rect x="3" y="11" width="2" height="2" fill="#E11D48" />
    <rect x="11" y="11" width="2" height="2" fill="#E11D48" />
  </svg>
);

export const PixelCoinIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg viewBox="0 0 16 16" shapeRendering="crispEdges" className={className} aria-hidden="true">
    <rect x="5" y="2" width="6" height="2" fill="#FDE68A" />
    <rect x="3" y="4" width="10" height="8" fill="#F5B942" />
    <rect x="5" y="12" width="6" height="2" fill="#C98A1B" />
    <rect x="7" y="5" width="2" height="6" fill="#C98A1B" />
  </svg>
);
