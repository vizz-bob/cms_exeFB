import { useEffect, useState } from "react";
import { Link } from "react-router-dom"; 
import { getResourcesPageData } from "../api";
import { motion } from "framer-motion";
import { 
    FileText, Download, ArrowRight, ExternalLink, 
    BookOpen, BarChart3, Link as LinkIcon, Newspaper,
    CheckCircle
} from "lucide-react";

// --- HELPER: Ensure URLs point to the Backend Server ---
const getDownloadUrl = (fileUrl) => {
    if (!fileUrl) return null;
    if (fileUrl.startsWith("http") || fileUrl.startsWith("//")) return fileUrl;

    const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
    const backendBase = isLocal ? "http://localhost:8000" : ""; 
    
    return `${backendBase}${fileUrl}`;
};

export default function Resources() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getResourcesPageData()
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Resources data fetch error:", err);
        setLoading(false);
      });
  }, []);

  // --- FUNCTION: Force file download ---
  const handleForceDownload = async (e, url, fileName) => {
    e.preventDefault(); 
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Network response was not ok");
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = fileName || "download"; 
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("Download failed, falling back to new tab:", error);
      window.open(url, "_blank");
    }
  };

  if (loading) return (
    <div className="h-screen flex items-center justify-center bg-white text-blue-600 font-mono animate-pulse">
        Loading Resources...
    </div>
  );

  const { hero, titles, latest_blogs, case_studies, downloads, useful_links } = data || {};

  return (
    <div className="min-h-screen bg-white overflow-x-hidden font-sans">
      
      {/* 1. HERO SECTION - BLUE FLUID GRADIENT THEME (MATCHING HOME) */}
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
                
                {/* Pill Badge - UPDATED: Blackish Background (bg-black/20) */}
                <div className="inline-flex flex-wrap justify-center items-center gap-3 py-1.5 px-5 rounded-full bg-black/20 backdrop-blur-md border border-white/10 text-blue-50 text-[10px] md:text-sm font-medium mb-8 shadow-lg">
                    <span className="flex items-center gap-1.5"><BarChart3 size={14} className="text-cyan-300"/> Case Studies</span> <span className="opacity-30">|</span> 
                    <span className="flex items-center gap-1.5"><FileText size={14} className="text-cyan-300"/> Templates</span> <span className="opacity-30">|</span> 
                    <span className="flex items-center gap-1.5"><Newspaper size={14} className="text-cyan-300"/> Insights</span>
                </div>

                {/* Heading - "Darker Shade of White" (Blue-50) */}
                <h1 className="text-4xl sm:text-5xl md:text-7xl font-bold mb-6 md:mb-8 leading-tight text-blue-50 drop-shadow-sm">
                    {hero?.title || "Knowledge Hub"}
                </h1>
                
                {/* Subtitle - "Darker Shade of White" (Blue-200) */}
                <p className="text-base sm:text-lg md:text-xl text-blue-200 mb-10 md:mb-12 max-w-3xl mx-auto leading-relaxed px-2 font-light tracking-wide">
                    {hero?.subtitle || "Insights, templates, and tools to empower your financial journey."}
                </p>
            </motion.div>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-6 py-20 space-y-24">
        
        {/* --- SECTION 1: LATEST BLOGS --- */}
        {latest_blogs?.length > 0 && (
            <section>
                <div className="flex justify-between items-end mb-10">
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-orange-100 rounded-lg text-orange-600">
                            <Newspaper size={28} />
                        </div>
                        <div>
                            <h2 className="text-3xl font-bold text-slate-900">Latest Insights</h2>
                            <p className="text-slate-500 text-sm mt-1">Updates on Tax, Compliance & Finance</p>
                        </div>
                    </div>
                    <Link to="/blog" className="hidden md:flex items-center text-blue-600 font-bold hover:translate-x-1 transition-transform">
                        View All Articles <ArrowRight size={20} className="ml-1" />
                    </Link>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {latest_blogs.map((blog, i) => (
                        <motion.div 
                            key={blog.id}
                            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
                            whileHover={{ y: -5 }}
                            className="bg-white rounded-xl shadow-md border border-slate-100 overflow-hidden flex flex-col h-full group"
                        >
                            <div className="h-40 bg-slate-100 overflow-hidden relative">
                                {blog.image ? (
                                    <img src={getDownloadUrl(blog.image)} alt={blog.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-slate-400 bg-slate-50">
                                        <Newspaper size={32} />
                                    </div>
                                )}
                            </div>
                            
                            <div className="p-5 flex flex-col flex-grow">
                                <span className="text-xs font-bold text-orange-600 uppercase tracking-wider mb-2 block">
                                    {blog.category?.name || "Update"}
                                </span>
                                <h3 className="font-bold text-lg text-slate-800 mb-3 line-clamp-2 leading-tight group-hover:text-blue-600 transition-colors">
                                    {blog.title}
                                </h3>
                                <p className="text-slate-500 text-sm line-clamp-2 mb-4 flex-grow">
                                    {blog.short_description}
                                </p>
                                <Link to={`/blog/${blog.slug}`} className="text-blue-600 font-semibold text-sm flex items-center mt-auto">
                                    Read More <ArrowRight size={16} className="ml-1" />
                                </Link>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </section>
        )}

        {/* --- SECTION 2: CASE STUDIES --- */}
        {case_studies?.length > 0 && (
          <section>
            <div className="flex items-center gap-3 mb-10">
                <div className="p-3 bg-blue-100 rounded-lg text-blue-600">
                    <BarChart3 size={28} />
                </div>
                <div>
                    <h2 className="text-3xl font-bold text-slate-900">{titles?.case_studies_title || "Success Stories"}</h2>
                    <p className="text-slate-500 text-sm mt-1">Real results from our partners.</p>
                </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8">
              {case_studies.map((cs, i) => (
                <motion.div 
                  key={cs.id} 
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} 
                  className="bg-white p-8 rounded-2xl shadow-lg border-l-4 border-blue-500 hover:shadow-xl transition-shadow relative overflow-hidden group"
                >
                  <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                      <FileText size={100} className="text-slate-400" />
                  </div>

                  <div className="flex justify-between items-start mb-4 relative z-10">
                    <div>
                        <h3 className="text-xl font-bold text-slate-800">{cs.title}</h3>
                        <p className="text-sm text-slate-500 font-medium mt-1">{cs.client_name}</p>
                    </div>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide border border-green-200">
                        {cs.result_stat}
                    </span>
                  </div>
                  
                  <p className="text-slate-600 mb-8 leading-relaxed relative z-10">{cs.summary}</p>
                  
                  {cs.pdf_file && (
                    <a 
                        href={getDownloadUrl(cs.pdf_file)} 
                        onClick={(e) => handleForceDownload(e, getDownloadUrl(cs.pdf_file), `${cs.title}.pdf`)}
                        className="inline-flex items-center text-blue-600 font-bold hover:text-blue-800 transition relative z-10 group/link cursor-pointer"
                    >
                      Read Full Story <ArrowRight size={18} className="ml-2 group-hover/link:translate-x-1 transition-transform" />
                    </a>
                  )}
                </motion.div>
              ))}
            </div>
          </section>
        )}

        {/* --- SECTION 3: DOWNLOADS --- */}
        {downloads?.length > 0 && (
          <section>
            <div className="flex items-center gap-3 mb-10">
                <div className="p-3 bg-purple-100 rounded-lg text-purple-600">
                    <BookOpen size={28} />
                </div>
                <div>
                    <h2 className="text-3xl font-bold text-slate-900">{titles?.downloads_title || "Templates & Guides"}</h2>
                    <p className="text-slate-500 text-sm mt-1">Ready-to-use resources for compliance.</p>
                </div>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {downloads.map((res, i) => {
                const finalUrl = getDownloadUrl(res.file) || res.external_link;
                const isExternal = !res.file && !!res.external_link;

                return (
                    <motion.div 
                    key={res.id} 
                    whileHover={{ y: -8 }} 
                    className="bg-white rounded-2xl shadow-md border border-slate-200 flex flex-col overflow-hidden"
                    >
                    <div className="p-6 flex-grow">
                        <div className="flex justify-between items-start mb-4">
                            <span className="bg-slate-100 text-slate-600 text-xs font-bold px-2 py-1 rounded uppercase tracking-wider">
                            {res.resource_type}
                            </span>
                        </div>
                        <h3 className="font-bold text-xl mb-3 text-slate-800">{res.title}</h3>
                        <p className="text-sm text-slate-500 leading-relaxed">{res.description}</p>
                    </div>
                    
                    <div className="p-6 pt-0 mt-auto border-t border-slate-100 bg-slate-50/50">
                        {finalUrl ? (
                            <a 
                            href={finalUrl} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            onClick={(e) => {
                                if (!isExternal) {
                                    handleForceDownload(e, finalUrl, res.title);
                                }
                            }}
                            className={`flex items-center justify-center gap-2 w-full py-3 rounded-xl font-semibold transition-all shadow-md active:scale-95 cursor-pointer ${
                                isExternal 
                                ? 'bg-white text-blue-600 border border-blue-200 hover:bg-blue-50' 
                                : 'bg-slate-900 text-white hover:bg-blue-600'
                            }`}
                            >
                            {isExternal ? <ExternalLink size={18} /> : <Download size={18} />} 
                            {isExternal ? "Access Resource" : "Download Now"}
                            </a>
                        ) : (
                            <button disabled className="w-full bg-gray-100 text-gray-400 py-3 rounded-xl cursor-not-allowed text-sm font-medium">
                            Coming Soon
                            </button>
                        )}
                    </div>
                    </motion.div>
                );
              })}
            </div>
          </section>
        )}

        {/* --- SECTION 4: USEFUL LINKS --- */}
        {useful_links?.length > 0 && (
          <section>
            <div className="flex items-center gap-3 mb-10">
                <div className="p-3 bg-teal-100 rounded-lg text-teal-600">
                    <LinkIcon size={28} />
                </div>
                <div>
                    <h2 className="text-3xl font-bold text-slate-900">Useful Links</h2>
                    <p className="text-slate-500 text-sm mt-1">Quick access to government and regulatory portals.</p>
                </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg border border-slate-100 overflow-hidden">
                <div className="grid md:grid-cols-2 lg:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-100">
                    {useful_links.map((link, i) => (
                        <a 
                            key={link.id} 
                            href={link.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="p-6 flex items-center justify-between hover:bg-slate-50 transition group border-b border-slate-100 md:border-b-0 last:border-b-0"
                        >
                            <span className="font-medium text-slate-700 group-hover:text-blue-600 transition-colors pr-4">
                                {link.title}
                            </span>
                            <ExternalLink size={18} className="text-slate-400 group-hover:text-blue-600 transition-colors shrink-0" />
                        </a>
                    ))}
                </div>
            </div>
          </section>
        )}

      </div>
    </div>
  );
}