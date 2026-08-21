import React from "react";
import { motion, useReducedMotion } from "framer-motion";

export function RagScene() {
  const reduce = useReducedMotion();
  const loop = (values, opts) => (reduce ? {} : { animate: { ...values }, transition: opts });

  return (
    <div className="landing-scene">
      <svg viewBox="0 0 800 460" preserveAspectRatio="xMidYMax slice">
        <defs>
          <linearGradient id="seaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#123d24" />
            <stop offset="100%" stopColor="#0a2417" />
          </linearGradient>
        </defs>

        <motion.g
          opacity={0.4}
          style={{ willChange: "transform" }}
          {...loop({ x: ["-15%", "115%"] }, { duration: 40, repeat: Infinity, ease: "linear" })}
        >
          <ellipse cx="120" cy="70" rx="60" ry="14" fill="#eafff0" />
        </motion.g>
        <motion.g
          opacity={0.3}
          style={{ willChange: "transform" }}
          {...loop({ x: ["-15%", "115%"] }, { duration: 60, repeat: Infinity, ease: "linear", delay: 2 })}
        >
          <ellipse cx="600" cy="110" rx="80" ry="16" fill="#eafff0" />
        </motion.g>

        <motion.circle
          cx="400" cy="210" r="120" fill="none" stroke="#f2b705" strokeWidth="1.5" strokeDasharray="2 14"
          style={{ transformOrigin: "400px 210px" }}
          {...loop({ opacity: [0.4, 0.8, 0.4], scale: [1, 1.05, 1] }, { duration: 4.5, repeat: Infinity, ease: "easeInOut" })}
        />
        <motion.circle
          cx="400" cy="210" r="78" fill="#f2b705"
          style={{ transformOrigin: "400px 210px" }}
          {...loop(
            { opacity: [0.92, 1, 0.92], filter: ["drop-shadow(0 0 22px rgba(242,183,5,0.6))", "drop-shadow(0 0 46px rgba(242,183,5,0.9))", "drop-shadow(0 0 22px rgba(242,183,5,0.6))"] },
            { duration: 4.5, repeat: Infinity, ease: "easeInOut" }
          )}
        />

        {[
          { d: "M250 90 q10 -10 20 0 q10 -10 20 0", delay: 0 },
          { d: "M320 60 q8 -8 16 0 q8 -8 16 0", delay: 1.8 },
          { d: "M480 100 q8 -8 16 0 q8 -8 16 0", delay: 3.4 },
        ].map((bird, i) => (
          <motion.g key={i} {...loop({ x: [0, 14, 0], y: [0, -8, 0] }, { duration: 5.5, repeat: Infinity, ease: "easeInOut", delay: bird.delay })}>
            <path d={bird.d} fill="none" stroke="#eafff0" strokeWidth="2" strokeLinecap="round" />
          </motion.g>
        ))}

        <rect x="0" y="210" width="800" height="130" fill="url(#seaGrad)" />
        {[
          { y: 240, opacity: 0.35, delay: 0, rev: false },
          { y: 268, opacity: 0.25, delay: 0.4, rev: true },
          { y: 296, opacity: 0.18, delay: 0.8, rev: false },
        ].map((band, i) => (
          <motion.path
            key={i}
            d={`M0 ${band.y} Q40 ${band.y - 10} 80 ${band.y} T160 ${band.y} T240 ${band.y} T320 ${band.y} T400 ${band.y} T480 ${band.y} T560 ${band.y} T640 ${band.y} T720 ${band.y} T800 ${band.y}`}
            fill="none" stroke="#3ef08a" strokeOpacity={band.opacity} strokeWidth="2" strokeDasharray="14 10"
            {...loop(
              { strokeDashoffset: band.rev ? [0, 240] : [0, -240] },
              { duration: band.rev ? 11 : 8, repeat: Infinity, ease: "linear", delay: band.delay }
            )}
          />
        ))}

        <motion.g {...loop({ y: [0, -6, 0] }, { duration: 3.4, repeat: Infinity, ease: "easeInOut" })}>
          <path d="M110 232 l34 0 l-6 10 l-22 0 z" fill="#0d1a11" stroke="#3ef08a" strokeWidth="1" />
          <line x1="127" y1="232" x2="127" y2="216" stroke="#3ef08a" strokeWidth="1.5" />
        </motion.g>

        <path d="M0 340 Q200 322 400 338 T800 336 L800 460 L0 460 Z" fill="#0d2417" />
        <path d="M0 340 Q200 322 400 338 T800 336" fill="none" stroke="#3ef08a" strokeOpacity="0.3" strokeWidth="2" />

        <g transform="translate(90,340) scale(1.15)">
          <path d="M0 120 C-6 80 -4 40 4 0" fill="none" stroke="#0a2417" strokeWidth="10" strokeLinecap="round" />
          <motion.g
            fill="#f2b705"
            style={{ transformBox: "fill-box", transformOrigin: "50% 100%" }}
            {...loop({ rotate: [-4, 4, -4] }, { duration: 6.5, repeat: Infinity, ease: "easeInOut" })}
          >
            <path d="M4 0 C-30 -6 -55 -22 -66 -46 C-38 -46 -12 -30 4 0Z" />
            <path d="M4 0 C36 -10 58 -30 66 -54 C36 -50 12 -30 4 0Z" />
            <path d="M4 0 C-14 -30 -14 -58 -2 -84 C16 -60 18 -30 4 0Z" />
            <path d="M4 0 C24 -22 44 -46 42 -74 C18 -60 4 -34 4 0Z" />
          </motion.g>
        </g>

        <g transform="translate(700,352) scale(-1.05,1.05)">
          <path d="M0 120 C-6 80 -4 40 4 0" fill="none" stroke="#0a2417" strokeWidth="9" strokeLinecap="round" />
          <motion.g
            fill="#f2b705"
            style={{ transformBox: "fill-box", transformOrigin: "50% 100%" }}
            {...loop({ rotate: [-4, 4, -4] }, { duration: 7.2, repeat: Infinity, ease: "easeInOut", delay: 1.2 })}
          >
            <path d="M4 0 C-30 -6 -55 -22 -66 -46 C-38 -46 -12 -30 4 0Z" />
            <path d="M4 0 C36 -10 58 -30 66 -54 C36 -50 12 -30 4 0Z" />
            <path d="M4 0 C-14 -30 -14 -58 -2 -84 C16 -60 18 -30 4 0Z" />
            <path d="M4 0 C24 -22 44 -46 42 -74 C18 -60 4 -34 4 0Z" />
          </motion.g>
        </g>

        <motion.g
          transform="translate(400,400)"
          style={{ transformBox: "fill-box", transformOrigin: "50% 100%" }}
          {...loop({ rotate: [-2, 2, -2] }, { duration: 5, repeat: Infinity, ease: "easeInOut" })}
        >
          <path d="M-46 40 L-40 0 L40 0 L46 40 Z" fill="#0e1611" stroke="#3ef08a" strokeOpacity="0.4" strokeWidth="1.5" />
          <path d="M-52 0 L0 -34 L52 0 Z" fill="#123d24" stroke="#3ef08a" strokeOpacity="0.5" strokeWidth="1.5" />
        </motion.g>
      </svg>
    </div>
  );
}
