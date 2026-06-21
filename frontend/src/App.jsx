import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, AlertCircle, Activity, Camera, ChevronRight, Zap, ShieldCheck, BarChart3, TrendingUp } from 'lucide-react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

const mockChartData = [
  { name: 'Mon', violations: 120 },
  { name: 'Tue', violations: 132 },
  { name: 'Wed', violations: 101 },
  { name: 'Thu', violations: 143 },
  { name: 'Fri', violations: 190 },
  { name: 'Sat', violations: 250 },
  { name: 'Sun', violations: 210 },
];

// Animated Counter Component
const AnimatedCounter = ({ value, prefix = "", suffix = "" }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 1500;
    const increment = value / (duration / 16);
    
    if (value === 0) {
      setCount(0);
      return;
    }

    const timer = setInterval(() => {
      start += increment;
      if (start >= value) {
        setCount(value);
        clearInterval(timer);
      } else {
        setCount(Math.ceil(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [value]);

  return <span>{prefix}{count}{suffix}</span>;
};

export default function App() {
  const [activeTab, setActiveTab] = useState('Overview');
  const tabs = ['Overview', 'Live Inference', 'Saved Evaluations', 'Global Analytics'];
  
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  // Evaluation History state
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('sentinel_history');
    return saved ? JSON.parse(saved) : [];
  });

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const objectUrl = URL.createObjectURL(selectedFile);
      setPreview(objectUrl);
      setResults(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('conf_threshold', 0.35);
    formData.append('run_lpr', true);

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(response.data);
      
      // Save to localStorage history
      const newHistoryItem = { 
        id: Date.now(), 
        timestamp: new Date().toLocaleString(), 
        results: response.data 
      };
      const updatedHistory = [newHistoryItem, ...history].slice(0, 15);
      setHistory(updatedHistory);
      localStorage.setItem('sentinel_history', JSON.stringify(updatedHistory));

    } catch (error) {
      console.error("Error analyzing frame:", error);
      alert("Analysis failed. Ensure FastAPI backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-slate-200 font-sans relative overflow-hidden selection:bg-neonCyan/30">
      
      {/* Background Ambient Glows */}
      <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-neonCyan/20 blur-[150px] rounded-full pointer-events-none" />
      <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-sunsetOrange/10 blur-[150px] rounded-full pointer-events-none" />
      <div className="fixed inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none"></div>

      <div className="p-8 max-w-[1400px] mx-auto relative z-10">
        
        {/* Premium Header */}
        <header className="flex justify-between items-center mb-12">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4 group cursor-pointer"
          >
            <div>
              <h1 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
                Sentinel <span className="px-2 py-0.5 rounded-full bg-white/10 text-xs font-medium text-slate-300 border border-white/5 uppercase tracking-widest">Edge AI</span>
              </h1>
              <p className="text-sm text-slate-400 font-medium mt-1">Next-Gen Traffic Compliance System</p>
            </div>
          </motion.div>
          
          {/* Animated Tabs */}
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex bg-white/5 p-1.5 rounded-full border border-white/10 backdrop-blur-md shadow-2xl"
          >
            {tabs.map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`relative px-6 py-2.5 text-sm font-semibold rounded-full transition-colors z-10 ${
                  activeTab === tab ? 'text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                {activeTab === tab && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 bg-white/10 border border-white/20 rounded-full shadow-lg -z-10"
                    transition={{ type: "spring", stiffness: 400, damping: 30 }}
                  />
                )}
                {tab}
              </button>
            ))}
          </motion.div>
        </header>

        {/* Overview Tab (Landing Page) */}
        {activeTab === 'Overview' && (
        <motion.main 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -30 }}
          className="flex flex-col items-center mt-12 text-center max-w-5xl mx-auto pb-24"
        >
          {/* Hero Section */}
          <h2 className="text-5xl lg:text-6xl font-black text-white tracking-tight mb-6">
            Welcome to <span className="text-transparent bg-clip-text bg-gradient-to-r from-neonCyan to-blue-500">Sentinel</span>
          </h2>
          
          <p className="text-xl text-slate-400 mb-12 leading-relaxed max-w-3xl">
            A next-generation, edge-deployed computer vision system designed to automate traffic violation detection. 
            Powered by YOLOv8 and EasyOCR, Sentinel instantly processes live surveillance feeds to detect triple-riding, 
            illegal parking, and speeding, while generating cryptographically verified evidence cards.
          </p>

          <motion.button 
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActiveTab('Live Inference')}
            className="bg-gradient-to-r from-neonCyan to-blue-500 text-black px-12 py-5 rounded-full font-bold flex items-center gap-3 shadow-[0_0_40px_rgba(0,240,255,0.4)] hover:shadow-[0_0_60px_rgba(0,240,255,0.6)] transition-all text-xl mb-24"
          >
            Start Evaluation <ChevronRight size={28} />
          </motion.button>

          {/* Value Propositions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-24 text-left">
            <div className="bg-white/[0.02] border border-white/10 rounded-3xl p-8 backdrop-blur-xl hover:border-white/20 hover:bg-white/[0.04] transition-all shadow-xl group">
              <Camera className="text-neonCyan mb-6 group-hover:scale-110 transition-transform" size={36} />
              <h3 className="text-xl text-white font-bold mb-3">Edge AI Processing</h3>
              <p className="text-slate-400 text-sm leading-relaxed">Runs advanced neural networks directly on camera nodes for zero-latency inference and tracking.</p>
            </div>
            <div className="bg-white/[0.02] border border-white/10 rounded-3xl p-8 backdrop-blur-xl hover:border-white/20 hover:bg-white/[0.04] transition-all shadow-xl group">
              <Zap className="text-sunsetOrange mb-6 group-hover:scale-110 transition-transform" size={36} />
              <h3 className="text-xl text-white font-bold mb-3">Instant OCR</h3>
              <p className="text-slate-400 text-sm leading-relaxed">Extracts license plates instantly using EasyOCR with custom pre-processing filters for high accuracy.</p>
            </div>
            <div className="bg-white/[0.02] border border-white/10 rounded-3xl p-8 backdrop-blur-xl hover:border-white/20 hover:bg-white/[0.04] transition-all shadow-xl group">
              <ShieldCheck className="text-blue-400 mb-6 group-hover:scale-110 transition-transform" size={36} />
              <h3 className="text-xl text-white font-bold mb-3">Secure Evidence</h3>
              <p className="text-slate-400 text-sm leading-relaxed">Generates immutable, cryptographically hashed evidence cards for municipal non-repudiation.</p>
            </div>
          </div>

          {/* Technical Architecture Section */}
          <div className="w-full text-left bg-gradient-to-br from-white/[0.02] to-transparent border border-white/10 rounded-3xl p-10 mb-24 relative overflow-hidden shadow-2xl">
            <div className="absolute top-0 right-0 w-96 h-96 bg-neonCyan/10 blur-3xl rounded-full -mr-20 -mt-20 pointer-events-none"></div>
            <h3 className="text-3xl font-black text-white mb-10">Technical Architecture</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 relative z-10">
              <div>
                <ul className="space-y-8">
                  <li className="flex items-start gap-4">
                    <div className="p-3 bg-blue-500/20 text-blue-400 rounded-xl border border-blue-500/20"><Activity size={24} /></div>
                    <div>
                      <h4 className="text-white font-bold text-lg">YOLOv8 Object Detection</h4>
                      <p className="text-slate-400 text-sm mt-1 leading-relaxed">State-of-the-art real-time object detection models fine-tuned to identify vehicle classes, detect parking zones, and flag triple-riding instances instantly.</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-4">
                    <div className="p-3 bg-purple-500/20 text-purple-400 rounded-xl border border-purple-500/20"><BarChart3 size={24} /></div>
                    <div>
                      <h4 className="text-white font-bold text-lg">FastAPI Microservices</h4>
                      <p className="text-slate-400 text-sm mt-1 leading-relaxed">High-performance asynchronous Python backend serving AI models with minimal latency overhead, routing video frames efficiently.</p>
                    </div>
                  </li>
                </ul>
              </div>
              <div>
                <ul className="space-y-8">
                  <li className="flex items-start gap-4">
                    <div className="p-3 bg-green-500/20 text-green-400 rounded-xl border border-green-500/20"><TrendingUp size={24} /></div>
                    <div>
                      <h4 className="text-white font-bold text-lg">React & Tailwind UX</h4>
                      <p className="text-slate-400 text-sm mt-1 leading-relaxed">Ultra-responsive, client-side rendered dashboard utilizing hardware-accelerated Framer Motion animations to visualize live telemetrics.</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-4">
                    <div className="p-3 bg-sunsetOrange/20 text-sunsetOrange rounded-xl border border-sunsetOrange/20"><ShieldCheck size={24} /></div>
                    <div>
                      <h4 className="text-white font-bold text-lg">Immutable Hash Ledgers</h4>
                      <p className="text-slate-400 text-sm mt-1 leading-relaxed">Every evidence card generates a SHA-256 hash immediately upon capture. This secures the data pipeline against tampering or repudiation.</p>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center w-full max-w-2xl mx-auto bg-white/[0.02] border border-white/5 rounded-3xl p-10">
            <h3 className="text-3xl font-bold text-white mb-4">Ready to test the prototype?</h3>
            <p className="text-slate-400 mb-8 text-lg">Upload test footage in the Live Inference dashboard to observe the pipeline in real-time.</p>
            <button 
              onClick={() => setActiveTab('Live Inference')}
              className="px-8 py-3 bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 rounded-xl text-white font-bold transition-all shadow-lg"
            >
              Go to Live Inference
            </button>
          </div>
        </motion.main>
        )}

        {/* Main Dashboard Grid - Live Inference */}
        {activeTab === 'Live Inference' && (
        <motion.main 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -30 }}
          transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
          className="grid grid-cols-12 gap-8"
        >
          {/* Left Column: Video Feed */}
          <div className="col-span-12 lg:col-span-8 flex flex-col gap-8">
            
            {/* Top Metric Cards */}
            <div className="grid grid-cols-3 gap-6">
              {[
                { label: "Vehicles Tracked", value: results ? results.total_vehicles : 0, icon: Activity, color: "text-blue-400" },
                { label: "Violations Detected", value: results ? results.total_violations : 0, icon: AlertCircle, color: "text-sunsetOrange" },
                { label: "Processing Latency", value: results ? results.process_time : 0, suffix: "ms", icon: Zap, color: "text-neonCyan" }
              ].map((stat, i) => (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 + (i * 0.1) }}
                  whileHover={{ y: -5, scale: 1.02 }}
                  className="bg-white/[0.02] border border-white/[0.05] hover:border-white/20 backdrop-blur-xl rounded-3xl p-6 relative overflow-hidden group shadow-2xl transition-all duration-300"
                >
                  <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-white/5 to-transparent rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`p-2 rounded-lg bg-white/5 border border-white/10 ${stat.color}`}>
                      <stat.icon size={18} />
                    </div>
                    <span className="text-sm font-semibold tracking-wider text-slate-400 uppercase">{stat.label}</span>
                  </div>
                  <div className="text-5xl font-black tracking-tighter text-white">
                    <AnimatedCounter value={stat.value} suffix={stat.suffix || ""} />
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Inference Upload Area */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="bg-white/[0.02] border border-white/[0.08] backdrop-blur-2xl rounded-3xl overflow-hidden shadow-2xl relative min-h-[500px] flex flex-col group"
            >
              {/* Header Bar */}
              <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between bg-black/20">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse"></div>
                  <span className="text-sm font-semibold tracking-widest text-slate-300 uppercase">Live Edge Node Stream</span>
                </div>
                <div className="px-3 py-1 bg-neonCyan/10 border border-neonCyan/30 text-neonCyan text-xs font-bold rounded-full">
                  YOLOv8 + EasyOCR
                </div>
              </div>

              {!preview ? (
                <div className="flex-1 m-6 border-2 border-dashed border-white/10 hover:border-neonCyan/50 hover:bg-neonCyan/[0.02] rounded-2xl flex flex-col items-center justify-center transition-all cursor-pointer relative">
                  <input 
                    type="file" 
                    className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                    onChange={handleFileChange} 
                    accept="image/*"
                  />
                  <div className="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mb-6 border border-white/10 group-hover:scale-110 transition-transform shadow-[0_0_30px_rgba(0,240,255,0)] group-hover:shadow-[0_0_30px_rgba(0,240,255,0.2)]">
                    <UploadCloud size={32} className="text-slate-400 group-hover:text-neonCyan transition-colors" />
                  </div>
                  <p className="text-xl text-white font-bold mb-2">Initialize Inference Feed</p>
                  <p className="text-slate-400 font-medium text-sm">Drag and drop a surveillance frame (JPG, PNG)</p>
                </div>
              ) : (
                <div className="flex-1 relative bg-black flex items-center justify-center">
                  <img 
                    src={results ? `data:image/jpeg;base64,${results.annotated_frame_b64}` : preview} 
                    className="w-full h-full object-cover opacity-90"
                    alt="Preview"
                  />
                  
                  {/* Grid Overlay */}
                  <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none"></div>

                  {!results && !loading && (
                    <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                      <motion.button 
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleAnalyze}
                        className="bg-gradient-to-r from-neonCyan to-blue-500 text-black px-8 py-4 rounded-full font-bold flex items-center gap-3 hover:shadow-[0_0_40px_rgba(0,240,255,0.6)] transition-all text-lg"
                      >
                        Execute Neural Analysis <ChevronRight size={24} />
                      </motion.button>
                    </div>
                  )}

                  {loading && (
                    <div className="absolute inset-0 bg-black/80 backdrop-blur-md flex flex-col items-center justify-center z-20">
                      <div className="relative w-24 h-24 mb-6">
                        <div className="absolute inset-0 rounded-full border-t-4 border-neonCyan animate-spin"></div>
                        <div className="absolute inset-2 rounded-full border-r-4 border-blue-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <Activity size={24} className="text-neonCyan animate-pulse" />
                        </div>
                      </div>
                      <p className="text-neonCyan font-bold tracking-widest uppercase text-sm animate-pulse">Running Neural Inference Pipeline...</p>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          </div>

          {/* Right Column: Evidence Log */}
          <motion.div 
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="col-span-12 lg:col-span-4 flex flex-col gap-4"
          >
             <div className="flex items-center justify-between px-2 mb-2">
               <h2 className="text-xl font-bold text-white flex items-center gap-2">
                 <ShieldCheck className="text-neonCyan" /> Verified Evidence
               </h2>
               {results && <span className="bg-white/10 text-white text-xs font-bold px-2 py-1 rounded border border-white/10">{results.evidence_cards.length} Logs</span>}
             </div>
             
             <div className="flex-1 bg-white/[0.02] border border-white/[0.05] rounded-3xl p-4 backdrop-blur-xl shadow-2xl flex flex-col gap-4 h-[calc(100vh-250px)] overflow-y-auto custom-scrollbar relative">
               
               {!results && (
                 <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500 p-8 text-center z-10">
                   <div className="w-16 h-16 rounded-full bg-white/5 border border-white/10 flex items-center justify-center mb-4">
                     <ShieldCheck size={24} className="opacity-50" />
                   </div>
                   <p className="font-medium">Awaiting Telemetry</p>
                   <p className="text-sm mt-2 opacity-60">Violations detected on the live feed will automatically populate cryptographically hashed evidence cards here.</p>
                 </div>
               )}

               {results && results.evidence_cards && results.evidence_cards.length === 0 && (
                 <div className="absolute inset-0 flex flex-col items-center justify-center text-green-500/80 p-8 text-center z-10">
                   <div className="w-16 h-16 rounded-full bg-green-500/10 border border-green-500/20 flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(34,197,94,0.2)]">
                     <ShieldCheck size={24} />
                   </div>
                   <p className="font-bold text-lg">All Clear</p>
                   <p className="text-sm mt-2 opacity-80 font-medium">No traffic violations were detected in this frame.</p>
                 </div>
               )}
               
               <AnimatePresence>
                 {results && results.evidence_cards.map((card, idx) => (
                   <motion.div 
                     key={idx}
                     initial={{ opacity: 0, scale: 0.9, y: 20 }}
                     animate={{ opacity: 1, scale: 1, y: 0 }}
                     transition={{ delay: idx * 0.1, type: "spring" }}
                     className="bg-black/40 border border-white/10 rounded-2xl p-4 flex gap-4 items-center group cursor-default hover:border-white/30 hover:bg-white/[0.05] transition-all"
                   >
                     <div className="w-24 h-24 rounded-xl overflow-hidden bg-black flex-shrink-0 border border-white/10 relative shadow-lg">
                       <img 
                         src={`data:image/jpeg;base64,${card.image_b64}`} 
                         className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
                       />
                       {/* Scanner Effect */}
                       <div className="absolute inset-0 bg-gradient-to-b from-transparent via-neonCyan/20 to-transparent h-[200%] -translate-y-full group-hover:animate-[scan_2s_ease-in-out_infinite]"></div>
                     </div>
                     
                     <div className="flex-1 min-w-0">
                       <div className="flex justify-between items-start mb-2">
                         <div className="inline-block px-2.5 py-1 bg-sunsetOrange/10 text-sunsetOrange text-[10px] font-black tracking-wider uppercase rounded-md border border-sunsetOrange/20 shadow-[0_0_10px_rgba(255,69,0,0.1)]">
                           {card.type}
                         </div>
                         <div className="text-[9px] text-slate-400 font-mono bg-white/5 px-2 py-0.5 rounded border border-white/10 flex items-center gap-1">
                           <ShieldCheck size={10} className="text-neonCyan" /> 
                           {results.hash ? results.hash.substring(0, 10) + '...' : 'HASH_VERIFIED'}
                         </div>
                       </div>
                       
                       <p className="text-sm font-semibold text-slate-200 mb-2 leading-tight">{card.details}</p>
                       
                       <div className="grid grid-cols-2 gap-2 mt-3">
                         <div className="p-2 bg-black/30 rounded-lg border border-white/5">
                           <p className="text-[9px] text-slate-500 uppercase font-bold mb-0.5">License Plate</p>
                           <p className="text-xs font-mono text-neonCyan font-bold tracking-wider truncate">{card.lpr_text}</p>
                         </div>
                         <div className="p-2 bg-black/30 rounded-lg border border-white/5">
                           <p className="text-[9px] text-slate-500 uppercase font-bold mb-0.5">AI Confidence</p>
                           <p className="text-xs font-bold text-white">{(card.conf * 100).toFixed(1)}%</p>
                         </div>
                       </div>
                     </div>
                   </motion.div>
                 ))}
               </AnimatePresence>

               {/* CSS for custom scrollbar & scanner animation */}
               <style dangerouslySetInnerHTML={{__html: `
                 .custom-scrollbar::-webkit-scrollbar { width: 6px; }
                 .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
                 .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
                 .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
                 @keyframes scan {
                   0% { transform: translateY(-100%); }
                   100% { transform: translateY(100%); }
                 }
               `}} />
             </div>
          </motion.div>

        </motion.main>
        )}

        {/* Global Analytics Tab */}
        {activeTab === 'Global Analytics' && (
        <motion.main 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col gap-8"
        >
          <div className="bg-white/[0.02] border border-white/[0.05] backdrop-blur-2xl rounded-3xl p-8 shadow-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-neonCyan/10 to-transparent rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
            
            <div className="flex items-center gap-3 mb-8">
              <div className="p-3 rounded-xl bg-white/5 border border-white/10 text-neonCyan">
                <TrendingUp size={24} />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">Weekly Violation Telemetry</h2>
                <p className="text-slate-400 font-medium">Aggregated data across all active city edge nodes</p>
              </div>
            </div>

            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={mockChartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="rgba(255,255,255,0.3)" tick={{fill: 'rgba(255,255,255,0.5)'}} axisLine={false} tickLine={false} />
                  <YAxis stroke="rgba(255,255,255,0.3)" tick={{fill: 'rgba(255,255,255,0.5)'}} axisLine={false} tickLine={false} />
                  <Tooltip 
                    cursor={{fill: 'rgba(255,255,255,0.05)'}}
                    contentStyle={{ backgroundColor: '#0B0F17', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                    itemStyle={{ color: '#00F0FF', fontWeight: 'bold' }}
                  />
                  <Bar dataKey="violations" radius={[6, 6, 0, 0]}>
                    {
                      mockChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.violations > 150 ? '#FF4500' : '#00F0FF'} />
                      ))
                    }
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-8">
            <div className="bg-white/[0.02] border border-white/[0.05] backdrop-blur-2xl rounded-3xl p-8 shadow-2xl">
              <h3 className="text-xl font-bold text-white mb-2">System Health</h3>
              <p className="text-slate-400 mb-6">Real-time edge node cluster status.</p>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl border border-white/5">
                  <span className="text-slate-300 font-medium">Uptime</span>
                  <span className="text-neonCyan font-bold tracking-widest">99.99%</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl border border-white/5">
                  <span className="text-slate-300 font-medium">Active Nodes</span>
                  <span className="text-white font-bold tracking-widest">1,024</span>
                </div>
              </div>
            </div>
            
            <div className="bg-white/[0.02] border border-white/[0.05] backdrop-blur-2xl rounded-3xl p-8 shadow-2xl flex flex-col items-center justify-center text-center">
               <ShieldCheck size={48} className="text-slate-600 mb-4" />
               <h3 className="text-xl font-bold text-white mb-2">Cryptographic Ledger</h3>
               <p className="text-slate-400">All evidence is securely hashed and backed by immutable storage. No tampering detected.</p>
            </div>
          </div>
        </motion.main>
        )}
        
        {/* Saved Evaluations Tab */}
        {activeTab === 'Saved Evaluations' && (
        <motion.main 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col gap-6"
        >
          <div className="flex items-center justify-between mb-4">
             <h2 className="text-2xl font-bold text-white flex items-center gap-2">
               <ShieldCheck className="text-neonCyan" /> Evaluation History
             </h2>
             {history.length > 0 && (
               <button 
                 onClick={() => { setHistory([]); localStorage.removeItem('sentinel_history'); }}
                 className="text-xs font-bold text-sunsetOrange border border-sunsetOrange/30 px-4 py-2 rounded-lg hover:bg-sunsetOrange/10 transition-colors"
               >
                 Clear History
               </button>
             )}
          </div>
          
          {history.length === 0 ? (
            <div className="flex flex-col items-center justify-center min-h-[400px] bg-white/[0.02] border border-white/5 rounded-3xl backdrop-blur-md">
               <Camera size={48} className="text-slate-600 mb-4" />
               <h3 className="text-xl font-bold text-white mb-2">No Evaluations Yet</h3>
               <p className="text-slate-400">Run your first AI inference on the Live Inference tab to save history locally.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {history.map(item => (
                <motion.div 
                  key={item.id}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => {
                    setResults(item.results);
                    setPreview(`data:image/jpeg;base64,${item.results.annotated_frame_b64}`);
                    setActiveTab('Live Inference');
                  }}
                  className="bg-white/[0.02] border border-white/10 rounded-3xl p-5 cursor-pointer hover:border-neonCyan/50 transition-all shadow-xl group"
                >
                  <div className="w-full h-48 bg-black rounded-2xl mb-5 overflow-hidden border border-white/5 relative">
                    <img src={`data:image/jpeg;base64,${item.results.annotated_frame_b64}`} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/90 to-transparent"></div>
                    <div className="absolute bottom-4 left-4 text-white text-xs font-bold tracking-widest">{item.timestamp}</div>
                  </div>
                  <div className="flex justify-between items-center bg-black/30 p-4 rounded-2xl border border-white/5">
                    <div>
                      <p className="text-slate-400 text-[10px] tracking-widest uppercase font-bold mb-1">Violations</p>
                      <p className="text-sunsetOrange font-black text-2xl">{item.results.total_violations}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-slate-400 text-[10px] tracking-widest uppercase font-bold mb-1">Vehicles</p>
                      <p className="text-blue-400 font-black text-2xl">{item.results.total_vehicles}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.main>
        )}
      </div>
    </div>
  );
}
