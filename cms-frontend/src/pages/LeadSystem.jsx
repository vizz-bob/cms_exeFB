import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getLeadSystemData } from "../api";
import * as LucideIcons from "lucide-react";
import { Link } from "react-router-dom";
import { ArrowRight, CheckCircle2, Zap } from "lucide-react";

export default function LeadSystem() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLeadSystemData()
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="h-screen flex items-center justify-center bg-white text-blue-600 font-mono animate-pulse">
        Loading System...
    </div>
  );

  const { hero, features, dashboard, cta } = data || {};

  const renderIcon = (name) => {
    const Icon = LucideIcons[name] || LucideIcons.Star;
    return <Icon size={32} />;
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20 font-sans">
      
      {/* 1. HERO SECTION - BLUE FLUID GRADIENT THEME (MATCHING RESOURCES) */}
      <section className="relative pt-32 pb-20 md:pt-44 md:pb-32 overflow-hidden px-4 bg-[#0a2463]">
        
        {/* BACKGROUND ART */}
        <div className="absolute inset-0 w-full h-full z-0">
            {/* Main Gradient Base */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-[#004aad] to-[#007aff] opacity-100"></div>
            
            {/* Striped Circle (Top Left) */}
            <div className="absolute -top-20 -left-20 w-80 h-80 rounded-full opacity-10 mix-blend-overlay"
                 style={{ backgroundImage: "repeating-linear-gradient(45deg, transparent, transparent 10px, #fff 10px, #fff 20px)" }}>
            </div>

            {/* Striped Corner (Bottom Right) */}
            <div className="absolute bottom-0 right-0 w-64 h-64 opacity-10 mix-blend-overlay z-0"
                 style={{ backgroundImage: "repeating-linear-gradient(-45deg, transparent, transparent 10px, #fff 10px, #fff 20px)" }}>
            </div>

            {/* Fluid Waves SVG */}
            <svg className="absolute top-0 left-0 w-full h-full opacity-40 pointer-events-none" viewBox="0 0 1440 800" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
                 <path d="M-66 358C-66 358 245 577 566 438C887 299 1109 417 1279 532C1449 647 1569 542 1569 542" stroke="url(#paint0_linear)" strokeWidth="80" strokeLinecap="round"/>
                 <path d="M-100 500C-100 500 300 300 700 550C1100 800 1400 400 1600 450" stroke="url(#paint1_linear)" strokeWidth="50" strokeOpacity="0.6"/>
                 <defs>
                    <linearGradient id="paint0_linear" x1="0" y1="0" x2="1000" y2="0" gradientUnits="userSpaceOnUse">
                        <stop stopColor="#3b82f6" stopOpacity="0"/>
                        <stop offset="0.5" stopColor="#60a5fa" stopOpacity="0.8"/>
                        <stop offset="1" stopColor="#93c5fd" stopOpacity="0"/>
                    </linearGradient>
                    <linearGradient id="paint1_linear" x1="0" y1="0" x2="1000" y2="0" gradientUnits="userSpaceOnUse">
                        <stop stopColor="#2563eb" stopOpacity="0"/>
                        <stop offset="0.5" stopColor="#1d4ed8" stopOpacity="0.5"/>
                        <stop offset="1" stopColor="#60a5fa" stopOpacity="0"/>
                    </linearGradient>
                 </defs>
            </svg>

            {/* Floating Bubbles/Dots */}
            <div className="absolute top-1/4 left-1/4 w-4 h-4 bg-blue-300 rounded-full blur-[1px] opacity-60 animate-pulse"></div>
            <div className="absolute top-1/3 right-1/4 w-8 h-8 bg-blue-400 rounded-full blur-[2px] opacity-40"></div>
            <div className="absolute bottom-1/3 left-1/3 w-20 h-20 bg-gradient-to-br from-blue-400 to-transparent rounded-full opacity-20 blur-xl"></div>
        </div>
        
        {/* CONTENT */}
        <div className="container mx-auto relative z-10 text-center max-w-4xl">
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
                
                {/* Pill Badge - Darker Background Style */}
                <div className="inline-flex items-center gap-2 py-1.5 px-5 rounded-full bg-black/20 backdrop-blur-md border border-white/10 text-blue-50 text-sm font-semibold mb-8 shadow-lg">
                    <Zap size={16} className="text-yellow-400 fill-yellow-400" />
                    <span>CRM & Automation</span>
                </div>

                {/* Heading - "Darker Shade of White" (Blue-50) */}
                <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-6 md:mb-8 leading-tight text-blue-50 drop-shadow-sm">
                    {hero?.title}
                </h1>
                
                {/* Subtitle - "Darker Shade of White" (Blue-200) */}
                <p className="text-base sm:text-lg md:text-xl text-blue-200 mb-10 max-w-2xl mx-auto leading-relaxed px-2 font-light tracking-wide">
                    {hero?.subtitle}
                </p>
            </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-6 mt-16 relative z-20">
        <div className="grid md:grid-cols-3 gap-8">
          {features?.map((item, i) => (
            <motion.div 
              key={item.id} 
              initial={{ opacity: 0, y: 20 }} 
              animate={{ opacity: 1, y: 0 }} 
              transition={{ delay: i * 0.1 }}
              whileHover={{ y: -10 }}
              className="bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-500 hover:shadow-2xl transition-all"
            >
              <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-600 mb-6 shadow-sm border border-blue-100">
                {renderIcon(item.icon_name)}
              </div>
              <h3 className="text-2xl font-bold text-slate-800 mb-3">{item.title}</h3>
              <p className="text-slate-600 leading-relaxed">{item.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Info Section with Dashboard Image */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <motion.div initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}>
            <h2 className="text-3xl font-bold text-slate-900 mb-6">Why Choose Our System?</h2>
            <ul className="space-y-4">
              {["Centralized Lead Database", "Automated Email Sequences", "Performance Analytics Dashboard", "Seamless Integration with Existing Tools"].map((point, idx) => (
                <li key={idx} className="flex items-center gap-3 text-slate-700 font-medium">
                  <CheckCircle2 className="text-green-500" size={20} /> {point}
                </li>
              ))}
            </ul>
          </motion.div>
          
          {/* DASHBOARD PREVIEW */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }} 
            whileInView={{ opacity: 1, scale: 1 }} 
            viewport={{ once: true }}
            className="bg-slate-100 rounded-3xl p-4 border border-slate-200 shadow-inner h-64 md:h-80 flex items-center justify-center overflow-hidden relative"
          >
            {dashboard?.image ? (
              <img 
                src={dashboard.image} 
                alt={dashboard.placeholder_text} 
                className="w-full h-full object-cover rounded-2xl shadow-lg"
              />
            ) : (
              <p className="text-slate-400 font-medium text-lg text-center px-4">
                {dashboard?.placeholder_text || "Dashboard Preview (Upload in Admin)"}
              </p>
            )}
          </motion.div>
        </div>
      </div>

      {/* CTA Section */}
      {cta && (
        <div className="max-w-5xl mx-auto px-6 mb-20">
          <div className="bg-gradient-to-r from-blue-600 to-purple-700 text-white p-12 md:p-16 rounded-3xl text-center shadow-2xl relative overflow-hidden">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 relative z-10">{cta.title}</h2>
            <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto relative z-10">{cta.text}</p>
            <Link to="/contact" className="inline-flex items-center gap-2 bg-white text-blue-700 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-transform hover:scale-105 shadow-lg relative z-10">
              {cta.button_text} <ArrowRight size={20} />
            </Link>
          </div>
        </div>
      )}

    </div>
  );
}