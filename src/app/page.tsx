'use client';

import { useState, useEffect, useRef } from 'react';
import { Upload, FileUp, FileType, CheckCircle, AlertCircle, Loader2, Download, FileSpreadsheet, Layers, Info, Plus } from 'lucide-react';

interface InputSlot {
  id: string;
  label: string;
  description: string;
  required: boolean;
  accept: string;
}

interface ReportConfig {
  name: string;
  input_slots: InputSlot[];
  expected_templates: Record<string, string[]>;
}

export default function Home() {
  const [reportTypes, setReportTypes] = useState<string[]>([]);
  const [selectedReport, setSelectedReport] = useState<string>('');
  const [sourceFiles, setSourceFiles] = useState<File[]>([]);
  const [existingExcel, setExistingExcel] = useState<File | null>(null);
  const [replaceWeek, setReplaceWeek] = useState<string>('');
  const [status, setStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState<string>('');
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const excelInputRef = useRef<HTMLInputElement>(null);

  // Fetch report types on mount
  useEffect(() => {
    fetch('/api/reports')
      .then(res => res.json())
      .then(data => {
        setReportTypes(data.reports || []);
        if (data.reports?.length > 0) setSelectedReport(data.reports[0]);
      })
      .catch(err => console.error('Failed to fetch reports:', err));
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSourceFiles(prev => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const handleExcelChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setExistingExcel(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent, type: 'source' | 'excel') => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      if (type === 'source') {
        setSourceFiles(prev => [...prev, ...Array.from(e.dataTransfer.files)]);
      } else {
        setExistingExcel(e.dataTransfer.files[0]);
      }
    }
  };

  const removeFile = (index: number) => {
    setSourceFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (sourceFiles.length === 0) {
      setMessage('Please upload at least one source file.');
      setStatus('error');
      return;
    }

    setStatus('processing');
    setMessage('Generating report...');
    setDownloadUrl(null);

    const formData = new FormData();
    formData.append('report_type', selectedReport);
    sourceFiles.forEach(file => formData.append('files', file));
    
    if (existingExcel) {
      formData.append('existing_excel', existingExcel);
    }
    if (replaceWeek) {
      formData.append('replace_week', replaceWeek);
    }

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Failed to generate report');
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
      setStatus('success');
      setMessage('Report generated successfully!');
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedReport}_report.xlsx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

    } catch (error: any) {
      console.error(error);
      setStatus('error');
      setMessage(error.message);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gradient-to-br from-gray-900 to-black text-white">
      <div className="container max-w-6xl mx-auto">
        <header className="mb-12 text-center fade-in">
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            Report Automation
          </h1>
          <p className="text-gray-400 text-lg">Generate complex reports with one click.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 fade-in">
          
          {/* Configuration Panel */}
          <div className="lg:col-span-4 card border-gray-800 bg-gray-900/50 backdrop-blur-xl h-fit">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <FileType className="w-5 h-5 text-blue-400" />
                Settings
              </h2>
              <a 
                href="/builder" 
                className="text-xs flex items-center gap-1 text-gray-400 hover:text-white transition-colors bg-gray-800/50 hover:bg-gray-800 px-3 py-1.5 rounded-full border border-gray-700"
              >
                <Plus size={12} /> Builder
              </a>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Report Type</label>
                <select 
                  className="select bg-gray-800 border-gray-700 focus:border-blue-500 w-full"
                  value={selectedReport}
                  onChange={(e) => setSelectedReport(e.target.value)}
                >
                  {reportTypes.map(type => (
                    <option key={type} value={type}>{type.replace(/-/g, ' ').toUpperCase()}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Optional: Week Replacement</label>
                <input 
                  type="text" 
                  placeholder="e.g., 05" 
                  className="input bg-gray-800 border-gray-700 focus:border-blue-500 w-full"
                  value={replaceWeek}
                  onChange={(e) => setReplaceWeek(e.target.value)}
                />
              </div>

              {replaceWeek && (
                <div className="animate-fade-in">
                 <input 
                   type="file" 
                   ref={excelInputRef}
                   className="hidden" 
                   accept=".xlsx,.xls"
                   onChange={handleExcelChange}
                 />
                 <div 
                 className={`drop-zone p-4 border-dashed border-2 rounded-lg transition-colors cursor-pointer ${existingExcel ? 'border-green-500 bg-green-500/10' : 'border-gray-700 hover:border-gray-500'}`}
                 onDragOver={e => e.preventDefault()}
                 onDrop={(e) => handleDrop(e, 'excel')}
                 onClick={() => excelInputRef.current?.click()}
               >
                 <div className="flex flex-col items-center gap-2 text-center">
                   <FileSpreadsheet className={`w-8 h-8 ${existingExcel ? 'text-green-400' : 'text-gray-500'}`} />
                   <span className="text-sm font-medium text-gray-300">
                     {existingExcel ? existingExcel.name : 'Drop Existing Excel Here'}
                   </span>
                 </div>
               </div>
               </div>
              )}
            </div>
            
            <button 
                onClick={handleSubmit}
                disabled={status === 'processing'}
                className={`btn btn-primary w-full mt-8 ${status === 'processing' ? 'opacity-70 cursor-wait' : ''}`}
            >
                {status === 'processing' ? (
                <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Processing...
                </>
                ) : (
                <>
                    <FileUp className="w-4 h-4" />
                    Generate Report
                </>
                )}
            </button>

            {status !== 'idle' && (
              <div className={`mt-6 p-4 rounded-lg flex flex-col gap-2 border ${
                status === 'success' ? 'bg-green-500/10 border-green-500/20 text-green-400' : 
                status === 'error' ? 'bg-red-500/10 border-red-500/20 text-red-400' : 
                'bg-blue-500/10 border-blue-500/20 text-blue-400'
              }`}>
                <div className="flex items-center gap-2">
                    {status === 'success' && <CheckCircle className="w-5 h-5 flex-shrink-0" />}
                    {status === 'error' && <AlertCircle className="w-5 h-5 flex-shrink-0" />}
                    {status === 'processing' && <Loader2 className="w-5 h-5 animate-spin flex-shrink-0" />}
                    <p className="text-sm font-medium">{message}</p>
                </div>
                 {downloadUrl && (
                  <a href={downloadUrl} download={`${selectedReport}_report.xlsx`} className="flex items-center gap-1 text-sm underline hover:no-underline self-end text-green-400">
                    <Download className="w-4 h-4" /> Download Again
                  </a>
                )}
              </div>
            )}
          </div>

          {/* Source Files Panel */}
          <div className="lg:col-span-8 space-y-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-white/90">
              <Layers className="w-5 h-5 text-purple-400" />
              Source Files
            </h2>
            
            <div className="card border-gray-800 bg-gray-900/50 backdrop-blur-xl">
                <input 
                    type="file" 
                    multiple 
                    ref={fileInputRef}
                    className="hidden" 
                    accept=".csv"
                    onChange={handleFileChange}
                />
                
                <div 
                    className={`drop-zone flex flex-col items-center justify-center gap-4 min-h-[200px] border-dashed border-2 rounded-xl transition-all cursor-pointer group ${
                        sourceFiles.length > 0 
                        ? 'border-purple-500/50 bg-purple-500/5' 
                        : 'border-gray-700 hover:border-purple-500 hover:bg-gray-800/50'
                    }`}
                    onDragOver={e => e.preventDefault()}
                    onDrop={(e) => handleDrop(e, 'source')}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <div className="p-4 bg-gray-800 rounded-full group-hover:scale-110 transition-transform">
                        <Upload className={`w-8 h-8 ${sourceFiles.length > 0 ? 'text-purple-400' : 'text-gray-400'}`} />
                    </div>
                    <div className="text-center">
                        <p className="text-lg font-medium text-gray-200">Click or Drag files here</p>
                        <p className="text-sm text-gray-500 mt-1">Accepts multiple .csv files</p>
                    </div>
                </div>

                {sourceFiles.length > 0 && (
                <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {sourceFiles.map((file, i) => (
                        <div key={i} className="bg-gray-800/50 border border-gray-700 p-3 rounded-lg flex items-center gap-3 animate-fade-in shadow-sm">
                            <FileSpreadsheet className="w-5 h-5 text-blue-400 flex-shrink-0" />
                            <div className="flex-1 min-w-0">
                                <p className="text-sm text-gray-200 truncate font-medium" title={file.name}>{file.name}</p>
                                <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
                            </div>
                            <button 
                                onClick={(e) => { e.stopPropagation(); removeFile(i) }}
                                className="text-gray-500 hover:text-red-400 p-1.5 hover:bg-red-500/10 rounded-full"
                            >
                                &times;
                            </button>
                        </div>
                    ))}
                </div>
                )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

