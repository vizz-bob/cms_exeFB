import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getServicesPageData } from "../api";
import { motion, AnimatePresence } from "framer-motion";
import * as LucideIcons from "lucide-react";
import { ArrowRight, Plus, Minus } from "lucide-react";

export default function Services() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeAccordion, setActiveAccordion] = useState(null);

  useEffect(() => {
    getServicesPageData().then((res) => { setData(res.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="h-screen flex items-center justify-center bg-white text-slate-600">Loading Services...</div>;

  const { hero, process, features, faq, cta, services_list } = data || {};
  const renderIcon = (iconName, size=24, className="") => {
    const Icon = LucideIcons[iconName] || LucideIcons.Briefcase;
    return <Icon size={size} className={className} />;
  };

  return (
    <div className="bg-slate-50 overflow-x-hidden font-sans">
      
      {/* HERO SECTION - MATCHING HOME THEME (Deep Blue + Fluid Waves) */}
      <section className="relative pt-32 pb-32 md:pt-44 md:pb-48 overflow-hidden px-4 bg-[#0a2463]">
        
        {/* BACKGROUND ART */}
        <div className="absolute inset-0 w-full h-full z-0 pointer-events-none">
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
            <svg className="absolute top-0 left-0 w-full h-full opacity-40" viewBox="0 0 1440 800" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
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

            {/* Floating Decoration Dots */}
            <div className="absolute top-1/4 left-1/4 w-4 h-4 bg-blue-300 rounded-full blur-[1px] opacity-60 animate-pulse"></div>
            <div className="absolute top-1/3 right-1/4 w-8 h-8 bg-blue-400 rounded-full blur-[2px] opacity-40"></div>
            <div className="absolute bottom-1/3 left-1/3 w-20 h-20 bg-gradient-to-br from-blue-400 to-transparent rounded-full opacity-20 blur-xl"></div>
        </div>

        {/* HERO CONTENT */}
        <div className="relative z-10 container mx-auto text-center px-4">
             <motion.h1 
               initial={{ opacity: 0, y: 30 }} 
               animate={{ opacity: 1, y: 0 }}
               transition={{ duration: 0.8 }}
               className="text-4xl md:text-6xl font-bold mb-6 text-blue-50 drop-shadow-sm"
             >
               {hero?.title || "Our Expertise"}
             </motion.h1>
             
             <motion.p 
                initial={{ opacity: 0, y: 20 }} 
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="text-lg md:text-xl text-blue-200 max-w-2xl mx-auto mb-10 font-light tracking-wide leading-relaxed"
             >
               {hero?.subtitle || "Comprehensive financial solutions tailored for your growth."}
             </motion.p>
        </div>
      </section>

      {/* SERVICES GRID (Offset upwards to overlap the dark hero) */}
      <div className="max-w-[90rem] mx-auto px-6 py-12 -mt-24 relative z-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {services_list?.map((service, index) => (
            <motion.div 
              key={service.id}
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.05 + 0.3 }}
              whileHover={{ y: -10 }}
              className="bg-white p-6 rounded-2xl shadow-xl border border-slate-100 group flex flex-col hover:shadow-2xl transition-all h-full"
            >
              <div className="w-14 h-14 bg-slate-50 rounded-xl flex items-center justify-center text-slate-500 mb-6 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                {renderIcon(service.icon, 28)}
              </div>
              <h3 className="text-xl font-bold text-slate-800 mb-3">{service.title}</h3>
              <p className="text-slate-600 text-sm mb-6 flex-grow line-clamp-3 leading-relaxed">{service.short_description}</p>
              
              <Link to={`/services/${service.slug}`} className="inline-flex items-center text-blue-600 font-bold text-sm group-hover:translate-x-2 transition-transform mt-auto">
                View Details <ArrowRight size={16} className="ml-2" />
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* PROCESS */}
      <section className="py-20 bg-white border-t border-slate-100">
        <div className="max-w-[90rem] mx-auto px-6">
            <h2 className="text-3xl font-bold text-center mb-16 text-slate-900">Our Process</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {process?.map((step, i) => (
                    <div key={i} className="text-center relative px-4">
                        <div className="w-20 h-20 mx-auto bg-blue-50 rounded-full flex items-center justify-center mb-6 text-blue-600 shadow-sm border border-blue-100">
                            {renderIcon(step.icon_name, 32)}
                        </div>
                        <h3 className="text-lg font-bold mb-2 text-slate-800">{step.step_number}. {step.title}</h3>
                        <p className="text-slate-600 text-sm leading-relaxed">{step.description}</p>
                    </div>
                ))}
            </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="py-20 bg-slate-100 text-slate-900">
        <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-3 gap-8">
            {features?.map((feat, i) => (
                <div key={i} className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                    {renderIcon(feat.icon_name, 32, "text-blue-600 mb-4")}
                    <h3 className="text-xl font-bold mb-2 text-slate-900">{feat.title}</h3>
                    <p className="text-slate-600">{feat.description}</p>
                </div>
            ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20 px-6 max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12 text-slate-900">Frequently Asked Questions</h2>
        <div className="space-y-4">
            {faq?.map((item, index) => (
                <div key={item.id} className="border border-slate-200 rounded-xl overflow-hidden bg-white shadow-sm">
                    <button onClick={() => setActiveAccordion(activeAccordion === index ? null : index)} className="w-full flex items-center justify-between p-5 text-left font-semibold text-slate-800 hover:bg-slate-50 transition">
                        {item.question}
                        {activeAccordion === index ? <Minus size={20} className="text-blue-600" /> : <Plus size={20} className="text-slate-400" />}
                    </button>
                    <AnimatePresence>
                        {activeAccordion === index && (
                            <motion.div initial={{ height: 0 }} animate={{ height: "auto" }} exit={{ height: 0 }} className="px-5 pb-5 text-slate-600 border-t border-slate-100">
                                {item.answer}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            ))}
        </div>
      </section>

      {/* CTA */}
      {cta && (
        <section className="py-20 px-6">
            <div className="max-w-5xl mx-auto bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-3xl p-12 text-center shadow-2xl relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10"></div>
                <h2 className="text-3xl font-bold mb-4 relative z-10">{cta.title}</h2>
                <p className="text-blue-100 mb-8 max-w-2xl mx-auto relative z-10">{cta.text}</p>
                <Link to="/contact" className="bg-white text-blue-700 px-8 py-3 rounded-full font-bold hover:bg-slate-100 transition shadow-lg relative z-10 hover:shadow-xl hover:-translate-y-1 inline-block">
                    {cta.button_text}
                </Link>
            </div>
        </section>
      )}
    </div>
  );
}