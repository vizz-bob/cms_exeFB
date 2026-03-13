import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getAboutPageData } from "../api"; 
import { Target, Eye, Heart, Award, ArrowRight, Cpu, Bot, Link as LinkIcon, ArrowDownCircle } from "lucide-react";
import * as LucideIcons from "lucide-react"; 
import { Link } from "react-router-dom";

export default function About() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAboutPageData()
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("About data error:", err);
        setLoading(false);
      });
  }, []);

  const renderDynamicIcon = (iconName) => {
    const IconComponent = LucideIcons[iconName] || LucideIcons.Cpu;
    // Icon inherits color from parent
    return <IconComponent size={40} className="mb-4 transition-colors duration-300" />;
  };

  if (loading) return <div className="h-screen flex items-center justify-center bg-white text-slate-600 animate-pulse">Loading About Page...</div>;

  const { content, team, awards, tech_stack } = data || {};

  return (
    <div className="min-h-screen bg-slate-50 overflow-hidden font-sans">
      
      {/* 1. HERO SECTION - BLUE FLUID GRADIENT THEME (Updated) */}
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
        <div className="container mx-auto relative z-10 text-center max-w-5xl">
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
                
                {/* Pill Badge (UPDATED: bg-black/20 for blackish tint) */}
                <div className="inline-flex flex-wrap justify-center items-center gap-3 py-1.5 px-5 rounded-full bg-black/20 backdrop-blur-md border border-white/20 text-blue-50 text-[10px] md:text-sm font-medium mb-8 shadow-lg">
                    <span className="flex items-center gap-1.5"><Cpu size={14} className="text-cyan-300"/> Innovation</span> <span className="opacity-30">|</span> 
                    <span className="flex items-center gap-1.5"><Bot size={14} className="text-cyan-300"/> Expertise</span> <span className="opacity-30">|</span> 
                    <span className="flex items-center gap-1.5"><LinkIcon size={14} className="text-cyan-300"/> Integrity</span>
                </div>

                {/* Heading - "Darker Shade of White" (Blue-50 / Slate-100) */}
                <h1 className="text-4xl sm:text-5xl md:text-7xl font-bold mb-6 md:mb-8 leading-tight text-blue-50 drop-shadow-sm">
                    {content?.hero_title || "About XpertAI"}
                </h1>
                
                {/* Subtitle - "Darker Shade of White" (Blue-200) */}
                <p className="text-base sm:text-lg md:text-xl text-blue-200 mb-10 md:mb-12 max-w-3xl mx-auto leading-relaxed px-2 font-light tracking-wide">
                    {content?.hero_subtitle || "Empowering businesses through next-generation financial intelligence."}
                </p>
                
                {/* Scroll Indicator */}
                <motion.div 
                    animate={{ y: [0, 10, 0] }} 
                    transition={{ repeat: Infinity, duration: 2 }}
                    className="flex justify-center mt-4"
                >
                    <ArrowDownCircle size={32} className="text-blue-300 opacity-60" />
                </motion.div>

            </motion.div>
        </div>
      </section>

      {/* i. COMPANY OVERVIEW */}
      <section className="py-20 px-6 max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
        <motion.div initial={{ x: -50, opacity: 0 }} whileInView={{ x: 0, opacity: 1 }} viewport={{ once: true }}>
          <h2 className="text-4xl font-bold text-slate-900 mb-6">{content?.story_title || "Company Overview"}</h2>
          <p className="text-slate-600 text-lg leading-relaxed whitespace-pre-line">
            {content?.story_text}
          </p>
        </motion.div>
        
        {/* IMAGE CONTAINER FIX */}
        <motion.div initial={{ scale: 0.8, opacity: 0 }} whileInView={{ scale: 1, opacity: 1 }} className="relative flex justify-center">
            {content?.story_image ? (
                <img 
                    src={content.story_image} 
                    alt="Overview" 
                    className="rounded-2xl shadow-2xl border border-slate-200 w-full h-auto object-contain max-h-[500px]" 
                />
            ) : (
                <div className="bg-blue-50 rounded-2xl h-80 w-full flex items-center justify-center border-2 border-dashed border-blue-200 text-blue-400 font-bold">
                    No Image Available
                </div>
            )}
        </motion.div>
      </section>

      {/* ii. MISSION, VISION & VALUES */}
      <div className="bg-white py-24 px-6 border-y border-slate-100">
        <div className="max-w-7xl mx-auto grid md:grid-cols-3 gap-8">
          {[
            { title: content?.mission_title, text: content?.mission_text, icon: Target, color: "text-blue-500" },
            { title: content?.vision_title, text: content?.vision_text, icon: Eye, color: "text-purple-500" },
            { title: content?.values_title, text: content?.values_text, icon: Heart, color: "text-pink-500" },
          ].map((item, i) => (
            <motion.div 
              key={i} whileHover={{ y: -10 }} 
              className="p-10 rounded-3xl bg-slate-50 border border-slate-100 shadow-sm hover:shadow-lg transition-all text-center"
            >
              <item.icon size={56} className={`${item.color} mx-auto mb-6`} />
              <h3 className="text-2xl font-bold text-slate-900 mb-4">{item.title}</h3>
              <p className="text-slate-600 leading-relaxed">{item.text}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* iii. LEADERSHIP */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">Leadership & Advisory Team</h2>
            <p className="text-slate-500">The experts driving our AI & Financial revolution.</p>
        </div>
        <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-8">
            {team?.map((member) => (
                <div key={member.id} className="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-100 group hover:shadow-xl transition-all">
                    <div className="h-64 overflow-hidden bg-slate-100 relative">
                        {member.image ? (
                            <img src={member.image} alt={member.name} className="w-full h-full object-cover transition duration-700 group-hover:scale-110" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-slate-400 bg-slate-50">No Photo</div>
                        )}
                    </div>
                    <div className="p-6 text-center">
                        <h3 className="text-xl font-bold text-slate-900">{member.name}</h3>
                        <p className="text-sm text-blue-600 font-medium uppercase tracking-wide mt-1">{member.role}</p>
                    </div>
                </div>
            ))}
        </div>
      </section>

      {/* iv. TECH STACK */}
      {tech_stack && tech_stack.length > 0 && (
        <section className="py-24 px-6 bg-slate-50 text-slate-900 relative overflow-hidden border-t border-slate-200">
            <div className="absolute inset-0 opacity-5 bg-[url('https://www.transparenttextures.com/patterns/circuit-board.png')]"></div>
            <div className="max-w-7xl mx-auto relative z-10">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Technology Stack</h2>
                    <p className="text-slate-500 max-w-2xl mx-auto">Built on the pillars of AI, Automation, and Blockchain.</p>
                </div>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {tech_stack.map((tech, index) => (
                        <motion.div 
                            key={tech.id}
                            initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.1 }}
                            className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-400 transition-all hover:-translate-y-2 group"
                        >
                            <div className="bg-blue-50 w-16 h-16 rounded-xl flex items-center justify-center mb-6 shadow-sm border border-blue-100 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300">
                                {renderDynamicIcon(tech.icon_name)}
                            </div>
                            <h3 className="text-xl font-bold mb-3 text-slate-900">{tech.title}</h3>
                            <p className="text-slate-500 text-sm leading-relaxed">{tech.description}</p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
      )}

      {/* EXTRA: AWARDS */}
      {awards && awards.length > 0 && (
        <section className="py-20 bg-blue-50 px-6">
            <div className="max-w-6xl mx-auto text-center">
                <h2 className="text-3xl font-bold mb-12 flex items-center justify-center gap-3">
                    <Award className="text-yellow-600" /> {content?.awards_title || "Recognition"}
                </h2>
                <div className="flex flex-wrap justify-center gap-6">
                    {awards.map((award) => (
                        <div key={award.id} className="bg-white px-8 py-6 rounded-xl shadow-sm border border-blue-100 flex flex-col items-center">
                            <span className="text-3xl font-bold text-blue-200 block mb-2">{award.year}</span>
                            <span className="font-bold text-slate-800">{award.title}</span>
                            <span className="text-xs text-slate-500">{award.description}</span>
                        </div>
                    ))}
                </div>
            </div>
        </section>
      )}

      {/* CTA */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-24 text-center px-6">
        <h2 className="text-4xl md:text-5xl font-bold mb-6">{content?.cta_title}</h2>
        <p className="mb-10 text-blue-100 text-lg">{content?.cta_text}</p>
        <Link to="/contact" className="inline-flex items-center bg-white text-blue-600 px-10 py-4 rounded-full font-bold transition shadow-lg hover:bg-slate-50">
            Contact Us <ArrowRight size={20} className="ml-2" />
        </Link>
      </div>
    </div>
  );
}