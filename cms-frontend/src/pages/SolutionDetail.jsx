import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getSolutionBySlug } from "../api";
import { motion } from "framer-motion";
import * as LucideIcons from "lucide-react";
import { ArrowLeft, CheckCircle2 } from "lucide-react";

export default function SolutionDetail() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    window.scrollTo(0, 0);
    getSolutionBySlug(slug)
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching solution:", err);
        setLoading(false);
      });
  }, [slug]);

  if (loading) return (
    <div className="h-screen flex items-center justify-center bg-white text-blue-600 font-bold animate-pulse">
        Loading Details...
    </div>
  );

  if (!data) return (
    <div className="h-screen flex flex-col items-center justify-center bg-white">
        <h2 className="text-2xl font-bold text-slate-800">Solution Not Found</h2>
        <Link to="/solutions" className="text-blue-600 mt-4 hover:underline">Back to Solutions</Link>
    </div>
  );

  const Icon = LucideIcons[data.icon_name] || LucideIcons.Layers;

  return (
    <div className="min-h-screen bg-slate-50 font-sans pb-20">
      
      {/* 1. HERO HEADER - LIGHT THEME */}
      <div className="bg-slate-50 text-slate-900 pt-40 pb-32 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-50"></div>
        
        <div className="max-w-6xl mx-auto relative z-10">
            <Link to="/solutions" className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-8 transition-colors group font-medium">
                <ArrowLeft size={20} className="mr-2 group-hover:-translate-x-1 transition-transform" /> Back to Solutions
            </Link>
            
            <div className="grid lg:grid-cols-2 gap-12 items-center">
                
                {/* TEXT CONTENT */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                    <div className="w-16 h-16 bg-white border border-slate-200 rounded-2xl flex items-center justify-center mb-6 shadow-sm">
                        <Icon size={32} className="text-blue-600" />
                    </div>
                    
                    <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight text-slate-900">
                        {data.title}
                    </h1>
                    <p className="text-xl text-slate-600 leading-relaxed mb-8">
                        {data.description}
                    </p>
                    
                    <Link to="/contact" className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-bold shadow-lg shadow-blue-200 transition-all hover:scale-105">
                        Start Now
                    </Link>
                </motion.div>

                {/* IMAGE or ICON VISUAL */}
                <motion.div 
                    initial={{ opacity: 0, scale: 0.9 }} 
                    animate={{ opacity: 1, scale: 1 }} 
                    transition={{ delay: 0.2 }}
                    className="relative flex justify-center"
                >
                    {/* Background blob behind image */}
                    <div className="absolute inset-0 bg-blue-200/30 rounded-full blur-3xl transform scale-75"></div>

                    {data.image ? (
                        <div className="relative rounded-3xl overflow-hidden shadow-2xl border border-slate-100 w-full max-w-lg aspect-video bg-white">
                            <img 
                                src={data.image} 
                                alt={data.title} 
                                className="w-full h-full object-cover"
                            />
                        </div>
                    ) : (
                        // Fallback if no image provided
                        <div className="relative bg-white p-12 rounded-3xl shadow-xl border border-slate-100 aspect-video flex flex-col items-center justify-center w-full max-w-lg text-slate-300">
                            <LucideIcons.Image size={64} className="mb-4 opacity-50" />
                            <span className="font-mono text-sm uppercase tracking-widest opacity-50">No Image Available</span>
                        </div>
                    )}
                </motion.div>

            </div>
        </div>
      </div>

      {/* 2. MAIN CONTENT AREA */}
      <div className="max-w-4xl mx-auto px-6 -mt-10 relative z-20">
        <motion.div 
            initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="bg-white p-8 md:p-12 rounded-3xl shadow-xl border border-slate-100"
        >
            <h2 className="text-2xl font-bold text-slate-900 mb-6 border-l-4 border-blue-500 pl-4">
                Detailed Overview
            </h2>
            
            <div className="prose prose-lg prose-slate text-slate-600 mb-10 whitespace-pre-line">
                {data.long_description ? (
                    data.long_description
                ) : (
                    <p className="italic text-slate-400">
                        Detailed description for this solution is coming soon.
                    </p>
                )}
            </div>
            
            {/* CTA BOX */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-2xl border border-blue-100 flex flex-col md:flex-row items-center justify-between gap-6">
                <div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">Ready to implement {data.title}?</h3>
                    <p className="text-slate-600">Our team is ready to help you get started.</p>
                </div>
                <Link to="/contact" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-blue-200 transition transform hover:-translate-y-1">
                    Get in Touch
                </Link>
            </div>
        </motion.div>
      </div>

    </div>
  );
}