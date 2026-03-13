import React, { useEffect, useState } from 'react';
import * as API from '../../../api'; 
import { 
  Save, Plus, Trash2, Edit2, Loader2, Image as ImageIcon, 
  X, Layout, Type, Link as LinkIcon
} from 'lucide-react';

export default function HomeManager() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('main'); 
  const [editingItem, setEditingItem] = useState(null);
  const [isAddingNew, setIsAddingNew] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await API.getHomeData();
      setData(res.data);
    } catch (err) {
      console.error("Failed to load home data", err);
    }
    setLoading(false);
  };

  // --- 1. SINGLETON CONTENT UPDATE (Hero, Titles, CTA) ---
  const handleMainContentUpdate = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const contentId = data.content?.id || 1;
        await API.updateHomeData(contentId, formData);
        alert("Main Content Updated Successfully!");
        loadData();
    } catch (err) {
        alert("Failed to update content. Make sure the backend is running.");
        console.error(err);
    }
  };

  // --- 2. GENERIC LIST HANDLERS ---
  const handleDelete = async (resource, id) => {
    if(!window.confirm("Are you sure you want to delete this item?")) return;
    try {
        await API.deleteItem(resource, id);
        loadData();
    } catch (err) { alert("Failed to delete."); }
  };

  const handleSaveItem = async (e, resource) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        if (editingItem) {
            await API.updateItem(resource, editingItem.id, formData);
        } else {
            await API.createItem(resource, formData);
        }
        setEditingItem(null);
        setIsAddingNew(false);
        loadData();
    } catch (err) {
        alert("Failed to save item.");
        console.error(err);
    }
  };

  if (loading) return <div className="flex justify-center items-center h-screen"><Loader2 className="animate-spin text-blue-600" size={40}/></div>;
  if (!data) return <div className="p-10 text-center">No data found. Please initialize the database.</div>;

  const tabs = [
      { id: 'main', label: 'Main Content & CTAs' },
      { id: 'process', label: 'Process Steps' },
      // Removed 'Key Services' tab
      { id: 'clients', label: 'Trusted Clients' },
      { id: 'testimonials', label: 'Testimonials' },
      { id: 'faq', label: 'FAQs' },
  ];

  return (
    <div className="max-w-7xl mx-auto pb-20 px-4 sm:px-6">
      
      {/* HEADER */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4 pt-6">
        <div>
            <h1 className="text-3xl font-bold text-slate-800 tracking-tight">Home Page Manager</h1>
            <p className="text-slate-500 text-sm mt-1">Manage content, buttons, and links</p>
        </div>
        <div className="flex flex-wrap gap-2 bg-white p-1 rounded-xl border border-slate-200 shadow-sm">
          {tabs.map(tab => (
              <button
                  key={tab.id}
                  onClick={() => { setActiveTab(tab.id); setEditingItem(null); setIsAddingNew(false); }}
                  className={`px-4 py-2 rounded-lg text-sm font-bold transition ${activeTab === tab.id ? 'bg-slate-900 text-white' : 'text-slate-500 hover:bg-slate-50'}`}
              >
                  {tab.label}
              </button>
          ))}
        </div>
      </div>

      {/* --- TAB 1: MAIN CONTENT (Singleton) --- */}
      {activeTab === 'main' && (
        <form onSubmit={handleMainContentUpdate} className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in">
            
            {/* 1. HERO SECTION */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4">
                <h3 className="text-lg font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
                    <Layout size={20} className="text-blue-600"/> Hero Section
                </h3>
                <div>
                    <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Hero Title</label>
                    <input name="hero_title" defaultValue={data.content?.hero_title} className="w-full border p-3 rounded-xl font-bold" />
                </div>
                <div>
                    <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Hero Subtitle</label>
                    <textarea name="hero_subtitle" defaultValue={data.content?.hero_subtitle} className="w-full border p-3 rounded-xl" rows="3"/>
                </div>
                
                <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-100">
                    <div className="col-span-2 text-xs font-bold text-blue-600 uppercase">Primary Button</div>
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Text</label>
                        <input name="hero_cta_text" defaultValue={data.content?.hero_cta_text} className="w-full border p-3 rounded-xl" />
                    </div>
                    <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Link</label>
                        <input name="hero_cta_link" defaultValue={data.content?.hero_cta_link} placeholder="/contact" className="w-full border p-3 rounded-xl" />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-100">
                    <div className="col-span-2 text-xs font-bold text-slate-500 uppercase">Secondary Button</div>
                    <div>
                         <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Text</label>
                        <input name="hero_sec_btn_text" defaultValue={data.content?.hero_sec_btn_text} placeholder="How It Works" className="w-full border p-3 rounded-xl" />
                    </div>
                </div>
            </div>

            {/* 2. SECTION HEADERS & AI */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4">
                <h3 className="text-lg font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
                    <Type size={20} className="text-slate-600"/> Section Headers & AI Selector
                </h3>
                <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 bg-slate-50 p-4 rounded-xl">
                        <div className="col-span-2 text-xs font-bold text-blue-600 uppercase">AI Recommendation Section</div>
                        <div className="col-span-2 md:col-span-1">
                             <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Title</label>
                             <input name="ai_title" defaultValue={data.content?.ai_title} className="w-full border p-3 rounded-xl" />
                        </div>
                        <div className="col-span-2 md:col-span-1">
                             <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Subtitle</label>
                             <input name="ai_subtitle" defaultValue={data.content?.ai_subtitle} className="w-full border p-3 rounded-xl" />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Process Title</label>
                            <input name="process_title" defaultValue={data.content?.process_title} className="w-full border p-3 rounded-xl" />
                        </div>
                        {/* Removed Services Title input */}
                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Clients Title</label>
                            <input name="clients_title" defaultValue={data.content?.clients_title} className="w-full border p-3 rounded-xl" />
                        </div>
                        {/* <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Reviews Title</label>
                            <input name="reviews_title" defaultValue={data.content?.reviews_title} className="w-full border p-3 rounded-xl" />
                        </div> */}
                        {/* <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Stories Title</label>
                            <input name="stories_title" defaultValue={data.content?.stories_title} className="w-full border p-3 rounded-xl" />
                        </div> */}
                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">FAQ Title</label>
                            <input name="faq_title" defaultValue={data.content?.faq_title} className="w-full border p-3 rounded-xl" />
                        </div>
                    </div>
                </div>
            </div>

            {/* 3. BOTTOM CTA / FOOTER (Consolidated) */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4 lg:col-span-2">
                <h3 className="text-lg font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
                    <LinkIcon size={20} className="text-blue-500"/> Bottom Call to Action (3 Buttons)
                </h3>
                <div className="grid md:grid-cols-2 gap-6">
                    {/* Header Info */}
                    <div className="md:col-span-2 grid md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Section Title</label>
                            <input name="cta_title" defaultValue={data.content?.cta_title} className="w-full border p-3 rounded-xl font-bold" />
                        </div>
                        <div>
                             <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Section Description</label>
                            <input name="cta_text" defaultValue={data.content?.cta_text} className="w-full border p-3 rounded-xl" />
                        </div>
                    </div>

                    <div className="md:col-span-2 border-t border-slate-100 my-2"></div>

                    {/* Button 1 */}
                    <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                        <div className="text-xs font-bold text-blue-600 uppercase mb-3">Button 1 (Left)</div>
                        <div className="space-y-3">
                            <div>
                                <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Text</label>
                                <input name="quick_link_1_text" defaultValue={data.content?.quick_link_1_text} placeholder="Sign Up" className="w-full border p-3 rounded-xl bg-white" />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Link</label>
                                <input name="quick_link_1_link" defaultValue={data.content?.quick_link_1_link} placeholder="/contact" className="w-full border p-3 rounded-xl bg-white" />
                            </div>
                        </div>
                    </div>

                    {/* Button 2 */}
                    <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                        <div className="text-xs font-bold text-blue-600 uppercase mb-3">Button 2 (Center)</div>
                        <div className="space-y-3">
                            <div>
                                <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Text</label>
                                <input name="quick_link_2_text" defaultValue={data.content?.quick_link_2_text} placeholder="Explore Services" className="w-full border p-3 rounded-xl bg-white" />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Link</label>
                                <input name="quick_link_2_link" defaultValue={data.content?.quick_link_2_link} placeholder="/services" className="w-full border p-3 rounded-xl bg-white" />
                            </div>
                        </div>
                    </div>

                    {/* Button 3 */}
                    <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 md:col-span-2 lg:col-span-1 lg:col-start-1 lg:col-end-3 xl:col-span-1 xl:col-auto">
                        <div className="text-xs font-bold text-blue-600 uppercase mb-3">Button 3 (Right)</div>
                        <div className="space-y-3">
                            <div>
                                <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Text</label>
                                <input name="quick_link_3_text" defaultValue={data.content?.quick_link_3_text} placeholder="Join as Professional" className="w-full border p-3 rounded-xl bg-white" />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Link</label>
                                <input name="quick_link_3_link" defaultValue={data.content?.quick_link_3_link} placeholder="/careers" className="w-full border p-3 rounded-xl bg-white" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="lg:col-span-2 flex justify-end sticky bottom-6 z-10">
                <button type="submit" className="bg-blue-600 text-white px-8 py-4 rounded-xl font-bold hover:bg-blue-700 shadow-xl transition flex items-center gap-2 transform hover:-translate-y-1">
                    <Save size={20}/> Save All Changes
                </button>
            </div>
        </form>
      )}

      {/* --- TABS FOR LISTS --- */}
      {activeTab === 'process' && (
        <ListManager 
            title="Process Steps" 
            items={data.process} 
            resource="process-steps" 
            fields={[
                { name: 'step_number', label: 'Step #', type: 'number' },
                { name: 'title', label: 'Title', type: 'text' },
                { name: 'description', label: 'Description', type: 'textarea' },
                { name: 'icon_name', label: 'Icon Name (Lucide)', type: 'text' },
            ]}
            onDelete={handleDelete}
            onSave={handleSaveItem}
            editingItem={editingItem}
            setEditingItem={setEditingItem}
            isAddingNew={isAddingNew}
            setIsAddingNew={setIsAddingNew}
        />
      )}

      {/* Removed 'Key Services' ListManager block */}

      {activeTab === 'clients' && (
        <ListManager 
            title="Trusted Clients" 
            items={data.clients} 
            resource="clients" 
            fields={[
                { name: 'name', label: 'Client Name', type: 'text' },
                { name: 'logo', label: 'Logo', type: 'file' },
                { name: 'order', label: 'Order Priority', type: 'number' },
            ]}
            onDelete={handleDelete}
            onSave={handleSaveItem}
            editingItem={editingItem}
            setEditingItem={setEditingItem}
            isAddingNew={isAddingNew}
            setIsAddingNew={setIsAddingNew}
        />
      )}

      {activeTab === 'testimonials' && (
        <ListManager 
            title="Testimonials" 
            items={data.testimonials} 
            resource="testimonials" 
            fields={[
                { name: 'author_name', label: 'Author Name', type: 'text' },
                { name: 'role', label: 'Role/Position', type: 'text' },
                { name: 'company', label: 'Company', type: 'text' },
                { name: 'quote', label: 'Quote', type: 'textarea' },
                { name: 'image', label: 'Author Photo', type: 'file' },
            ]}
            onDelete={handleDelete}
            onSave={handleSaveItem}
            editingItem={editingItem}
            setEditingItem={setEditingItem}
            isAddingNew={isAddingNew}
            setIsAddingNew={setIsAddingNew}
        />
      )}

      {activeTab === 'faq' && (
        <ListManager 
            title="Frequently Asked Questions" 
            items={data.faq} 
            resource="faqs" 
            fields={[
                { name: 'question', label: 'Question', type: 'text' },
                { name: 'answer', label: 'Answer', type: 'textarea' },
                { name: 'order', label: 'Order', type: 'number' },
            ]}
            onDelete={handleDelete}
            onSave={handleSaveItem}
            editingItem={editingItem}
            setEditingItem={setEditingItem}
            isAddingNew={isAddingNew}
            setIsAddingNew={setIsAddingNew}
        />
      )}

    </div>
  );
}

// ============================================================================
// SUB-COMPONENT: GENERIC LIST MANAGER
// ============================================================================
const ListManager = ({ title, items, resource, fields, onDelete, onSave, editingItem, setEditingItem, isAddingNew, setIsAddingNew }) => {
    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <h2 className="text-xl font-bold text-slate-800">{title} ({items?.length || 0})</h2>
                {!isAddingNew && !editingItem && (
                    <button onClick={() => setIsAddingNew(true)} className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 hover:bg-blue-700 transition shadow-md">
                        <Plus size={18}/> Add New
                    </button>
                )}
            </div>

            {/* EDIT / ADD FORM */}
            {(isAddingNew || editingItem) && (
                <form onSubmit={(e) => onSave(e, resource)} className="bg-slate-50 p-6 rounded-2xl border border-blue-200 shadow-sm mb-6">
                    <div className="flex justify-between items-center mb-4 border-b border-slate-200 pb-2">
                        <h3 className="font-bold text-blue-700">{editingItem ? 'Edit Item' : 'Add New Item'}</h3>
                        <button type="button" onClick={() => { setEditingItem(null); setIsAddingNew(false); }} className="bg-white p-1 rounded-full hover:bg-slate-200"><X size={20}/></button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {fields.map(field => (
                            <div key={field.name} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
                                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">{field.label}</label>
                                {field.type === 'textarea' ? (
                                    <textarea name={field.name} defaultValue={editingItem?.[field.name]} className="w-full border p-3 rounded-xl" rows="3" required/>
                                ) : field.type === 'file' ? (
                                    <div className="flex items-center gap-4">
                                        {editingItem?.[field.name] && <img src={editingItem[field.name]} alt="preview" className="h-12 w-12 rounded-lg object-cover border"/>}
                                        <input type="file" name={field.name} className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"/>
                                    </div>
                                ) : (
                                    <input type={field.type} name={field.name} defaultValue={editingItem?.[field.name]} className="w-full border p-3 rounded-xl" required={field.type !== 'file'} />
                                )}
                            </div>
                        ))}
                    </div>
                    <div className="mt-6 flex justify-end gap-3">
                        <button type="button" onClick={() => { setEditingItem(null); setIsAddingNew(false); }} className="px-4 py-2 text-slate-600 font-bold hover:bg-slate-200 rounded-lg">Cancel</button>
                        <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded-lg font-bold flex items-center gap-2 hover:bg-blue-700 shadow-md">
                            <Save size={18}/> Save Item
                        </button>
                    </div>
                </form>
            )}

            {/* LIST DISPLAY */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {items && items.map(item => (
                    <div key={item.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition group relative">
                        <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity bg-white p-1 rounded-lg shadow-sm border z-10">
                            <button onClick={() => { setEditingItem(item); setIsAddingNew(false); window.scrollTo({top:0, behavior:'smooth'}); }} className="text-blue-600 p-1 hover:bg-blue-50 rounded"><Edit2 size={16}/></button>
                            <button onClick={() => onDelete(resource, item.id)} className="text-red-500 p-1 hover:bg-red-50 rounded"><Trash2 size={16}/></button>
                        </div>

                        <div className="pr-12">
                            {(item.image || item.logo) && (
                                <img src={item.image || item.logo} alt="img" className="h-10 w-10 object-contain mb-3 rounded-lg bg-slate-50 border"/>
                            )}
                            <h4 className="font-bold text-slate-800 line-clamp-1">{item.title || item.name || item.author_name || item.question || item.value}</h4>
                            <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                                {item.description || item.quote || item.answer || item.label || item.role}
                            </p>
                            {item.step_number && <span className="text-[10px] font-bold bg-slate-100 px-2 py-1 rounded mt-2 inline-block">Step {item.step_number}</span>}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};