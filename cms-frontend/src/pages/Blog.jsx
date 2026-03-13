import { useEffect, useState } from "react";
import { Link } from "react-router-dom"; 
import { getBlogs, getCategories } from "../api"; 
import { motion, AnimatePresence } from "framer-motion";
import { Calendar, Search, ArrowRight, BookOpen, Clock, Filter, X, ChevronRight, Newspaper } from "lucide-react"; 
import usePageContent from "../hooks/usePageContent"; 

// Simple placeholder icon component for fallback images
const ImageIcon = ({ size }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ opacity: 0.2 }}>
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <circle cx="8.5" cy="8.5" r="1.5"></circle>
        <polyline points="21 15 16 10 5 21"></polyline>
    </svg>
);

export default function Blog() {
  const { getField } = usePageContent("blog"); 
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  
  const [selectedCategory, setSelectedCategory] = useState(null); // Slug of selected category
  const [searchQuery, setSearchQuery] = useState(""); 
  
  const [loading, setLoading] = useState(true);

  // Toggle category selection
  const handleCategoryClick = (slug) => {
    setSelectedCategory(currentSlug => currentSlug === slug ? null : slug);
  };

  // 1. Fetch Categories from Admin/API
  useEffect(() => {
    getCategories()
      .then((res) => {
          // Ensure we handle different API response structures (e.g. pagination)
          const data = Array.isArray(res.data) ? res.data : (res.data.results || []);
          setCategories(data);
      })
      .catch(err => console.error("Error fetching categories:", err));
  }, []);

  // 2. Fetch Blogs (Filtered by Category & Search)
  useEffect(() => {
    setLoading(true);
    // Debounce search to prevent too many API calls while typing
    const timer = setTimeout(() => {
        getBlogs(selectedCategory, searchQuery)
          .then((res) => { 
            const data = Array.isArray(res.data) ? res.data : (res.data.results || []);
            setPosts(data); 
          })
          .catch(err => {
              console.error("Error fetching blogs:", err);
              setPosts([]);
          })
          .finally(() => {
            setLoading(false);
          });
    }, 400); 
    
    return () => clearTimeout(timer);
  }, [selectedCategory, searchQuery]); 
  
  const currentFilterName = categories.find(cat => cat.slug === selectedCategory)?.name;

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      
      {/* --- HERO SECTION - BLUE FLUID GRADIENT THEME (MATCHING RESOURCES) --- */}
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
                
                {/* Pill Badge - Darkish Glassmorphism */}
                <div className="inline-flex flex-wrap justify-center items-center gap-3 py-1.5 px-5 rounded-full bg-black/20 backdrop-blur-md border border-white/10 text-blue-50 text-[10px] md:text-sm font-medium mb-8 shadow-lg">
                    <span className="flex items-center gap-1.5"><Newspaper size={14} className="text-cyan-300"/> Our Journal</span> <span className="opacity-30">|</span> 
                    <span className="flex items-center gap-1.5">Expert Analysis</span>
                </div>

                {/* Heading - "Darker Shade of White" (Blue-50) */}
                <h1 className="text-4xl sm:text-5xl md:text-7xl font-bold mb-6 md:mb-8 leading-tight text-blue-50 drop-shadow-sm">
                    {getField("hero_title", "title") || "Insights & Ideas"}
                </h1>
                
                {/* Subtitle - "Darker Shade of White" (Blue-200) */}
                <p className="text-base sm:text-lg md:text-xl text-blue-200 mb-10 md:mb-12 max-w-3xl mx-auto leading-relaxed px-2 font-light tracking-wide">
                    {getField("hero_text") || "Explore the latest trends, expert analysis, and actionable advice from our team."}
                </p>
            </motion.div>
        </div>
      </section>

      {/* --- STICKY TOOLBAR (Filter & Search) --- */}
      <div className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-200 shadow-sm transition-all duration-300">
        <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
                
                {/* Categories - Horizontal Scroll */}
                <div className="w-full md:w-auto flex items-center gap-2 overflow-x-auto no-scrollbar pb-2 md:pb-0 mask-gradient pr-4">
                    <div className="flex items-center text-slate-400 mr-2 flex-shrink-0">
                        <Filter size={16} />
                    </div>
                    
                    <button
                        onClick={() => setSelectedCategory(null)}
                        className={`whitespace-nowrap px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 border ${
                            selectedCategory === null 
                            ? 'bg-slate-900 text-white border-slate-900 shadow-md transform scale-105' 
                            : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                        }`}
                    >
                        All Stories
                    </button>

                    {categories.map((cat) => (
                        <button
                            key={cat.id} 
                            onClick={() => handleCategoryClick(cat.slug)}
                            className={`whitespace-nowrap px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 border ${
                                selectedCategory === cat.slug 
                                ? 'bg-blue-600 text-white border-blue-600 shadow-md transform scale-105' 
                                : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                            }`}
                        >
                            {cat.name}
                        </button>
                    ))}
                </div>

                {/* Search Input */}
                <div className="w-full md:w-80 relative group">
                    <input 
                        type="text" 
                        placeholder="Search articles..." 
                        className="w-full pl-10 pr-10 py-2.5 bg-slate-100 border border-transparent rounded-xl text-sm font-medium focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all placeholder:text-slate-400"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    <Search className="absolute left-3.5 top-2.5 text-slate-400 group-focus-within:text-blue-500 transition-colors" size={18} />
                    {searchQuery && (
                        <button onClick={() => setSearchQuery("")} className="absolute right-3 top-2.5 text-slate-400 hover:text-red-500 transition-colors">
                            <X size={16} />
                        </button>
                    )}
                </div>
            </div>
        </div>
      </div>

      {/* --- BLOG GRID --- */}
      <div className="max-w-7xl mx-auto px-6 py-12 min-h-[60vh]">
          
          <div className="flex items-center gap-2 mb-8 text-sm text-slate-500 font-medium">
             {selectedCategory && (
                 <>
                    <span>Filtering by: <span className="text-blue-600 font-bold">{currentFilterName}</span></span>
                    <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
                 </>
             )}
             <span>{posts.length} Result{posts.length !== 1 && 's'}</span>
          </div>

          {loading ? (
             <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                 {[1,2,3,4,5,6].map(i => (
                     <div key={i} className="bg-white rounded-[2rem] h-[450px] animate-pulse border border-slate-200 shadow-sm"></div>
                 ))}
             </div>
          ) : posts.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-32 text-center animate-in fade-in zoom-in-95 duration-500">
                <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mb-6 shadow-inner">
                    <BookOpen size={40} className="text-slate-300" />
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-2">No articles found</h3>
                <p className="text-slate-500 max-w-md mx-auto mb-8">
                    We couldn't find anything matching "{searchQuery}" {selectedCategory ? `in ${currentFilterName}` : ''}.
                </p>
                <button 
                    onClick={() => { setSearchQuery(""); setSelectedCategory(null); }}
                    className="px-8 py-3 bg-slate-900 text-white rounded-xl text-sm font-bold hover:bg-slate-800 transition shadow-lg hover:shadow-slate-900/20 active:scale-95"
                >
                    Clear Filters
                </button>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {posts.map((blog, i) => (
                <motion.article 
                  key={blog.id} 
                  initial={{ opacity: 0, y: 20 }} 
                  animate={{ opacity: 1, y: 0 }} 
                  transition={{ delay: i * 0.05 }}
                  className="group bg-white rounded-[2rem] border border-slate-100 shadow-[0_10px_30px_-10px_rgba(0,0,0,0.05)] hover:shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] hover:-translate-y-2 transition-all duration-500 ease-out flex flex-col h-full overflow-hidden"
                >
                  {/* Image Container */}
                  <Link to={`/blog/${blog.slug}`} className="block h-56 overflow-hidden relative">
                      {blog.image ? (
                          <img 
                            src={blog.image} 
                            alt={blog.title} 
                            className="w-full h-full object-cover transform group-hover:scale-110 transition duration-700 ease-in-out" 
                          />
                      ) : (
                          <div className="w-full h-full bg-slate-100 flex items-center justify-center text-slate-300">
                              <ImageIcon size={48} />
                          </div>
                      )}
                      
                      {/* Gradient Overlay */}
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-60"></div>

                      {/* Floating Category Badge */}
                      {blog.category_name && ( 
                        <div className="absolute top-4 left-4">
                            <span className="bg-white/95 backdrop-blur-md text-slate-900 text-[10px] uppercase font-bold px-3 py-1.5 rounded-full shadow-lg border border-white/20 tracking-wider">
                                {blog.category_name}
                            </span>
                        </div>
                      )}
                  </Link>

                  {/* Content Container */}
                  <div className="p-6 md:p-8 flex flex-col flex-grow relative">
                    
                    {/* Meta Info */}
                    <div className="flex items-center gap-3 text-xs font-semibold text-slate-400 mb-4 uppercase tracking-wider">
                        <span className="flex items-center gap-1.5">
                            <Calendar size={12} className="text-blue-500" /> 
                            {new Date(blog.published_date || blog.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                        </span>
                        <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                        <span className="flex items-center gap-1.5">
                            <Clock size={12} className="text-blue-500" /> 
                            {Math.ceil((blog.content?.length || 1000) / 1000)} min read
                        </span>
                    </div>

                    {/* Title */}
                    <Link to={`/blog/${blog.slug}`} className="block group-hover:text-blue-600 transition-colors duration-300">
                        <h3 className="text-xl font-bold text-slate-900 mb-3 leading-tight line-clamp-2">
                            {blog.title}
                        </h3>
                    </Link>

                    {/* Description */}
                    <p className="text-slate-600 text-sm leading-relaxed mb-6 line-clamp-3 flex-grow">
                        {blog.short_description || "Read more about this interesting topic..."}
                    </p>
                    
                    {/* Footer */}
                    <div className="pt-6 mt-auto border-t border-slate-50 flex items-center justify-between">
                      <div className="flex items-center gap-2.5">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-slate-200 to-slate-300 flex items-center justify-center text-[10px] font-bold text-slate-600 shadow-inner">
                              AI
                          </div>
                          <span className="text-xs font-bold text-slate-700">XpertAI Team</span>
                      </div>

                      <Link to={`/blog/${blog.slug}`} className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 uppercase tracking-wider hover:gap-2 transition-all group/link">
                          Read <ArrowRight size={14} className="group-hover/link:translate-x-1 transition-transform" />
                      </Link>
                    </div>
                  </div>
                </motion.article>
              ))}
            </div>
          )}
      </div>
    </div>
  );
}