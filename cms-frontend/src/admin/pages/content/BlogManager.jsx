import React, { useEffect, useState } from 'react';
import * as API from '../../../api'; 
import { Plus, Edit2, Trash2, Loader2, Save, X, Image as ImageIcon, Folder, FileText } from 'lucide-react';

export default function BlogManager() {
  const [blogs, setBlogs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('blogs'); 
  
  // Edit State
  const [editingBlog, setEditingBlog] = useState(null);
  const [editingCategory, setEditingCategory] = useState(null);
  const [isAddingCategory, setIsAddingCategory] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [blogRes, catRes] = await Promise.all([API.getBlogs(), API.getCategories()]);
      setBlogs(blogRes.data.results || blogRes.data || []);
      setCategories(catRes.data.results || catRes.data || []); 
    } catch (err) {
      console.error("Failed to load blog data", err);
    }
    setLoading(false);
  };

  // --- BLOG HANDLERS ---
  const handleDeleteBlog = async (id) => {
    if(!window.confirm("Are you sure you want to delete this post?")) return;
    try {
        await API.deleteBlog(id);
        setBlogs(prev => prev.filter(b => b.id !== id));
        alert("Blog deleted successfully.");
    } catch (err) { alert("Failed to delete blog."); }
  };

  const handleSaveBlog = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    // 1. Handle Checkbox
    if (!formData.has('published')) formData.append('published', 'False');
    else formData.set('published', 'True');

    // 2. FIX: Handle Image Update Logic
    // If the user didn't upload a NEW file, the size will be 0.
    // We must remove it so Django uses the existing image instead of crashing.
    const imageFile = formData.get('image');
    if (imageFile && imageFile.size === 0) {
        formData.delete('image');
    }

    try {
      if (editingBlog.id) {
          // Update existing
          await API.updateBlog(editingBlog.id, formData);
      } else {
          // Create new
          await API.createBlog(formData);
      }
      
      alert("Blog Post Saved!");
      setEditingBlog(null);
      loadData();
    } catch (err) { 
        console.error(err);
        // Show the actual error message from backend if available
        const msg = err.response?.data ? JSON.stringify(err.response.data) : "Error saving blog.";
        alert(msg); 
    }
  };

  // --- CATEGORY HANDLERS ---
  const handleSaveCategory = async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      
      try {
          if (editingCategory) {
              await API.updateItem('blog/categories', editingCategory.id, formData);
          } else {
              await API.createItem('blog/categories', formData);
          }
          alert("Category Saved!");
          setEditingCategory(null);
          setIsAddingCategory(false);
          loadData();
      } catch (err) {
          console.error(err);
          alert("Failed to save category. Ensure name is unique.");
      }
  };

  const handleDeleteCategory = async (id) => {
      if(!window.confirm("Delete this category? Posts in this category may become uncategorized.")) return;
      try {
          await API.deleteItem('blog/categories', id);
          loadData();
      } catch (err) { alert("Failed to delete category."); }
  };


  if (loading && !editingBlog) return <div className="flex h-screen items-center justify-center"><Loader2 className="animate-spin text-blue-600" size={40}/></div>;

  // --- BLOG EDITOR VIEW ---
  if (editingBlog) {
    return (
      <div className="max-w-5xl mx-auto pb-20 animate-in fade-in zoom-in-95 duration-300">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-slate-800">{editingBlog.id ? 'Edit Blog Post' : 'New Blog Post'}</h2>
          <button onClick={() => setEditingBlog(null)} className="bg-white p-2 rounded-full shadow-sm hover:bg-slate-100 transition"><X size={24} className="text-slate-600"/></button>
        </div>

        <form onSubmit={handleSaveBlog} className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Post Title</label>
              <input name="title" defaultValue={editingBlog.title} required className="w-full p-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none font-bold text-lg" placeholder="Enter title..."/>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Category</label>
              {/* FIX: Ensure defaultValue handles objects or IDs correctly */}
              <select 
                name="category" 
                defaultValue={typeof editingBlog.category === 'object' ? editingBlog.category?.id : editingBlog.category} 
                className="w-full p-3 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="">-- Select Category --</option>
                {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>

          {/* Image Upload */}
          <div>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Cover Image</label>
              <div className="flex items-center gap-6 bg-slate-50 p-4 rounded-xl border border-slate-200">
                  {editingBlog.image && (
                      <div className="relative group">
                        <img src={editingBlog.image} alt="Preview" className="h-24 w-32 object-cover rounded-lg shadow-sm bg-white"/>
                        <div className="absolute inset-0 bg-black/50 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition text-white text-xs">Current</div>
                      </div>
                  )}
                  <div className="flex-1">
                    <input type="file" name="image" className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 transition cursor-pointer"/>
                    <p className="text-xs text-slate-400 mt-2">Leave empty to keep current image</p>
                  </div>
              </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Short Description</label>
            <textarea name="short_description" rows="2" defaultValue={editingBlog.short_description} className="w-full p-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Brief summary..."/>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Full Content</label>
            <textarea name="body" rows="12" defaultValue={editingBlog.body} required className="w-full p-4 border border-slate-200 rounded-xl font-mono text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Write content here..."/>
          </div>
          <div className="flex items-center gap-3 bg-blue-50 p-4 rounded-xl border border-blue-100">
            <input type="checkbox" id="published" name="published" defaultChecked={editingBlog.published} className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"/>
            <label htmlFor="published" className="font-bold text-slate-700 cursor-pointer select-none">Publish immediately?</label>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
             <button type="button" onClick={() => setEditingBlog(null)} className="px-6 py-3 text-slate-600 font-bold hover:bg-slate-100 rounded-xl transition">Cancel</button>
             <button type="submit" className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-blue-700 flex items-center gap-2 shadow-lg transition transform active:scale-95">
                <Save size={20}/> Save Post
             </button>
          </div>
        </form>
      </div>
    );
  }

  // --- MAIN LIST VIEW ---
  return (
    <div className="max-w-7xl mx-auto pb-20 space-y-8 px-6">
      
      {/* HEADER & TABS */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
            <h1 className="text-3xl font-bold text-slate-800">Blog Manager</h1>
            <p className="text-slate-500 mt-1">Manage articles and categories.</p>
        </div>
        <div className="flex gap-2 bg-white p-1 rounded-xl border border-slate-200">
            <button 
                onClick={() => { setActiveTab('blogs'); setIsAddingCategory(false); setEditingCategory(null); }} 
                className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition ${activeTab === 'blogs' ? 'bg-slate-900 text-white' : 'text-slate-500 hover:bg-slate-50'}`}
            >
                <FileText size={16}/> Posts
            </button>
            <button 
                onClick={() => setActiveTab('categories')} 
                className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition ${activeTab === 'categories' ? 'bg-slate-900 text-white' : 'text-slate-500 hover:bg-slate-50'}`}
            >
                <Folder size={16}/> Categories
            </button>
        </div>
      </div>

      {/* --- BLOGS TAB --- */}
      {activeTab === 'blogs' && (
          <div className="space-y-6 animate-in fade-in">
              <div className="flex justify-end">
                  <button onClick={() => setEditingBlog({})} className="bg-blue-600 text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2 hover:bg-blue-700 shadow-lg transition">
                    <Plus size={20}/> New Post
                  </button>
              </div>

              <div className="grid gap-4">
                {blogs.map(blog => (
                  <div key={blog.id} className="bg-white p-5 rounded-xl border border-slate-200 flex flex-col md:flex-row md:items-center justify-between hover:shadow-md transition group">
                    <div className="flex items-center gap-5">
                      <img src={blog.image || '/placeholder.png'} alt={blog.title} className="w-20 h-20 rounded-lg object-cover bg-slate-100 border border-slate-100"/>
                      <div>
                        <h3 className="font-bold text-lg text-slate-800 group-hover:text-blue-600 transition">{blog.title}</h3>
                        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1">
                          <span className="bg-slate-100 px-2.5 py-1 rounded-md font-medium text-slate-600 border border-slate-200">
                            {blog.category_name || 'Uncategorized'}
                          </span>
                          <span>{new Date(blog.published_date || blog.created_at).toLocaleDateString()}</span>
                          <span className={`flex items-center gap-1 font-bold ${blog.published ? "text-emerald-600" : "text-amber-500"}`}>
                            <span className={`w-2 h-2 rounded-full ${blog.published ? "bg-emerald-500" : "bg-amber-500"}`}></span>
                            {blog.published ? "Published" : "Draft"}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex gap-2 mt-4 md:mt-0 pl-0 md:pl-4 border-t md:border-t-0 border-slate-100 pt-4 md:pt-0">
                      <button onClick={() => setEditingBlog(blog)} className="p-2.5 text-blue-600 hover:bg-blue-50 rounded-lg transition" title="Edit">
                        <Edit2 size={18}/>
                      </button>
                      <button onClick={() => handleDeleteBlog(blog.id)} className="p-2.5 text-red-600 hover:bg-red-50 rounded-lg transition" title="Delete">
                        <Trash2 size={18}/>
                      </button>
                    </div>
                  </div>
                ))}
                
                {blogs.length === 0 && (
                    <div className="text-center py-16 bg-slate-50 rounded-2xl border-2 border-dashed border-slate-300">
                        <p className="text-slate-400 font-medium">No blog posts found.</p>
                    </div>
                )}
              </div>
          </div>
      )}

      {/* --- CATEGORIES TAB --- */}
      {activeTab === 'categories' && (
          <div className="space-y-6 animate-in fade-in">
              <div className="flex justify-between items-center">
                  <h3 className="text-xl font-bold text-slate-700">All Categories</h3>
                  {!isAddingCategory && !editingCategory && (
                      <button onClick={() => setIsAddingCategory(true)} className="bg-blue-600 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 hover:bg-blue-700 shadow-md transition">
                        <Plus size={18}/> Add Category
                      </button>
                  )}
              </div>

              {/* Category Form */}
              {(isAddingCategory || editingCategory) && (
                  <form onSubmit={handleSaveCategory} className="bg-slate-50 p-6 rounded-2xl border border-blue-200 shadow-sm mb-6 animate-in zoom-in-95">
                      <div className="flex justify-between items-center mb-4 border-b border-slate-200 pb-2">
                          <h3 className="font-bold text-blue-700">{editingCategory ? 'Edit Category' : 'New Category'}</h3>
                          <button type="button" onClick={() => { setEditingCategory(null); setIsAddingCategory(false); }} className="bg-white p-1 rounded-full hover:bg-slate-200"><X size={20}/></button>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                          <div>
                              <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Category Name</label>
                              <input name="name" defaultValue={editingCategory?.name} className="w-full border p-3 rounded-xl bg-white" required placeholder="e.g. AI Technology"/>
                          </div>
                          <div>
                              <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Slug (Optional)</label>
                              <input name="slug" defaultValue={editingCategory?.slug} className="w-full border p-3 rounded-xl bg-white" placeholder="Auto-generated if empty"/>
                          </div>
                      </div>
                      <div className="mt-6 flex justify-end gap-3">
                          <button type="button" onClick={() => { setEditingCategory(null); setIsAddingCategory(false); }} className="px-4 py-2 text-slate-600 font-bold hover:bg-slate-200 rounded-lg">Cancel</button>
                          <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded-lg font-bold flex items-center gap-2 hover:bg-blue-700 shadow-md">
                              <Save size={18}/> Save Category
                          </button>
                      </div>
                  </form>
              )}

              {/* Category List */}
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {categories.map(cat => (
                      <div key={cat.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex justify-between items-center group hover:shadow-md transition">
                          <div>
                              <h4 className="font-bold text-slate-800">{cat.name}</h4>
                              <p className="text-xs text-slate-400 font-mono mt-1">/{cat.slug}</p>
                          </div>
                          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                              <button onClick={() => { setEditingCategory(cat); setIsAddingCategory(false); }} className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"><Edit2 size={16}/></button>
                              <button onClick={() => handleDeleteCategory(cat.id)} className="p-2 text-red-600 hover:bg-red-50 rounded-lg"><Trash2 size={16}/></button>
                          </div>
                      </div>
                  ))}
                  {categories.length === 0 && !isAddingCategory && (
                      <div className="col-span-full text-center py-10 text-slate-400 border-2 border-dashed border-slate-200 rounded-xl">
                          No categories found.
                      </div>
                  )}
              </div>
          </div>
      )}

    </div>
  );
}