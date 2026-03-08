'use client';

import { useState, useCallback } from 'react';
import { 
  Plus, 
  Trash2, 
  ChevronRight, 
  ChevronLeft, 
  Upload, 
  FileText, 
  Layout, 
  Settings, 
  Save, 
  CheckCircle2, 
  AlertCircle,
  ArrowLeft,
  FileSpreadsheet,
  Layers
} from 'lucide-react';
import Link from 'next/link';

type Step = 'setup' | 'analyze' | 'sheets' | 'campaigns' | 'templates' | 'weeks' | 'review';

export default function BuilderPage() {
  const [currentStep, setCurrentStep] = useState<Step>('setup');
  const [config, setConfig] = useState({
    id: '',
    name: '',
    description: '',
    campaign_mappings: [] as any[],
    template_mappings: [] as any[],
    target_sheet: '',
    label_column: 'B',
    week_columns: { mappings: {} } as any,
    metrics: {
      row_structure: [
        { offset: 0, name: 'Sent', type: 'data' },
        { offset: 1, name: 'Delivered', type: 'data' },
        { offset: 2, name: 'Opened', type: 'data' },
        { offset: 3, name: 'Clicked', type: 'data' },
        { offset: 4, name: 'Unsubscribed', type: 'data' },
        { offset: 5, name: '% Delivered', type: 'formula' },
        { offset: 6, name: '% Open', type: 'formula' },
        { offset: 7, name: '% Click', type: 'formula' }
      ]
    }
  });

  const [files, setFiles] = useState<File[]>([]);
  const [excelFile, setExcelFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<any>(null);


  const nextStep = () => {
    if (currentStep === 'setup') setCurrentStep('analyze');
    else if (currentStep === 'analyze') setCurrentStep('sheets');
    else if (currentStep === 'sheets') handleDiscoverLabels();
    else if (currentStep === 'campaigns') setCurrentStep('templates');
    else if (currentStep === 'templates') setCurrentStep('weeks');
    else if (currentStep === 'weeks') setCurrentStep('review');
  };

  const prevStep = () => {
    if (currentStep === 'analyze') setCurrentStep('setup');
    else if (currentStep === 'sheets') setCurrentStep('analyze');
    else if (currentStep === 'campaigns') setCurrentStep('sheets');
    else if (currentStep === 'templates') setCurrentStep('campaigns');
    else if (currentStep === 'weeks') setCurrentStep('templates');
    else if (currentStep === 'review') setCurrentStep('weeks');
  };

  const handleAnalyze = async () => {
    if (files.length === 0 || !excelFile) {
      alert('Please upload CSV and Excel files for analysis.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    formData.append('excel_file', excelFile);

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setAnalysis(data);
      
      // Auto-initialize mappings if possible
      const allCampaigns = Array.from(new Set(data.csv_analysis.flatMap((c: any) => c.campaigns)));
      const initialCampaignMappings = allCampaigns.map((c: any) => ({
        campaign_name: c,
        target_sheet: data.excel_analysis.sheets[0]?.name || '',
        start_row: 3,
        has_aggregate_row: true
      }));
      
      setConfig(prev => ({ 
        ...prev, 
        campaign_mappings: initialCampaignMappings,
        target_sheet: data.excel_analysis.sheets[0]?.name || ''
      }));
      nextStep();
    } catch (error) {
      console.error('Analysis failed', error);
      alert('Analysis failed. Check console.');
    } finally {
      setLoading(false);
    }
  };

  const handleDiscoverLabels = async () => {
    if (!excelFile || !config.target_sheet) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('excel_file', excelFile);
    formData.append('sheet_name', config.target_sheet);
    formData.append('column_letter', config.label_column);

    try {
      const res = await fetch('/api/analyze-sheet', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      
      // Update analysis with new labels for the selected sheet
      const updatedAnalysis = { ...analysis };
      const sheetIdx = updatedAnalysis.excel_analysis.sheets.findIndex((s: any) => s.name === config.target_sheet);
      if (sheetIdx !== -1) {
        updatedAnalysis.excel_analysis.sheets[sheetIdx].column_b = data.labels; // reusing column_b field for simplicity in UI
      }
      setAnalysis(updatedAnalysis);
      
      // Initialize template mappings
      const allTemplates = Array.from(new Set(analysis.csv_analysis.flatMap((c: any) => c.templates)));
      const initialTemplateMappings = config.campaign_mappings.map(c => ({
        campaign_name: c.campaign_name,
        templates: []
      }));
      setConfig(prev => ({ ...prev, template_mappings: initialTemplateMappings }));
      
      if (currentStep === 'sheets') setCurrentStep('campaigns');
    } catch (error) {
      console.error('Label discovery failed', error);
      alert('Failed to discover labels. Check console.');
    } finally {
      setLoading(false);
    }
  };

  const saveConfig = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('config', JSON.stringify(config));
      
      const res = await fetch('/api/report-types', {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        setStatus({ type: 'success', message: 'Report type saved successfully!' });
      } else {
        setStatus({ type: 'error', message: 'Failed to save report type.' });
      }
    } catch (error) {
      setStatus({ type: 'error', message: 'Error saving report type.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 bg-gradient-to-br from-gray-900 to-black text-white font-sans">
      <div className="container max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-12 fade-in">
          <div className="flex items-center gap-4">
            <Link href="/" className="p-2 hover:bg-gray-800 rounded-full transition-all border border-transparent hover:border-gray-700">
              <ArrowLeft size={20} className="text-blue-400" />
            </Link>
            <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
              Report Builder
            </h1>
          </div>
          <div className="flex gap-2">
            {(['setup', 'analyze', 'sheets', 'campaigns', 'templates', 'weeks', 'review'] as Step[]).map((s, i) => (
              <div 
                key={s} 
                className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${currentStep === s ? 'bg-blue-500 ring-4 ring-blue-500/20 scale-125' : i < (['setup', 'analyze', 'sheets', 'campaigns', 'templates', 'weeks', 'review'] as Step[]).indexOf(currentStep) ? 'bg-blue-900' : 'bg-gray-800'}`}
              />
            ))}
          </div>
        </div>

        <div className="card border-gray-800 bg-gray-900/50 backdrop-blur-xl overflow-hidden fade-in shadow-2xl">
          {/* Step content */}
          <div className="p-8">
            {currentStep === 'setup' && (
              <div className="space-y-6 fade-in">
                <div>
                  <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <Settings className="text-blue-400 w-6 h-6" /> Basic Information
                  </h2>
                  <p className="text-gray-400 text-sm mb-6">Initialize your new report configuration with a unique identifier.</p>
                </div>
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-400">Report ID (Slug)</label>
                    <input 
                      type="text" 
                      placeholder="e.g. slot-report"
                      className="input bg-gray-800 border-gray-700 focus:border-blue-500"
                      value={config.id}
                      onChange={e => setConfig({ ...config, id: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-400">Display Name</label>
                    <input 
                      type="text" 
                      placeholder="e.g. Weekly Slot Report"
                      className="input bg-gray-800 border-gray-700 focus:border-blue-500"
                      value={config.name}
                      onChange={e => setConfig({ ...config, name: e.target.value })}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-400">Description</label>
                  <textarea 
                    placeholder="Briefly describe what this report covers..."
                    className="input bg-gray-800 border-gray-700 focus:border-blue-500 h-24 resize-none"
                    value={config.description}
                    onChange={e => setConfig({ ...config, description: e.target.value })}
                  />
                </div>
                <div className="flex justify-end pt-4">
                  <button 
                    onClick={nextStep}
                    disabled={!config.id || !config.name}
                    className="btn btn-primary px-10 py-3 shadow-lg shadow-blue-500/20"
                  >
                    Next: Upload Samples <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'analyze' && (
              <div className="space-y-8 fade-in">
                <div>
                  <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <Upload className="text-purple-400 w-6 h-6" /> Upload Sample Files
                  </h2>
                  <p className="text-gray-400 text-sm">We need sample CSVs and a target Excel template to map the structures.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* CSV Upload */}
                  <div className="space-y-4">
                    <label className="text-sm font-bold flex items-center gap-2 text-gray-300">
                      <FileText size={18} className="text-blue-400" /> Source CSV Files
                    </label>
                    <div 
                      className={`drop-zone p-8 border-dashed border-2 rounded-2xl transition-all cursor-pointer group relative ${files.length > 0 ? 'border-blue-500/50 bg-blue-500/5' : 'border-gray-800 hover:border-blue-500 bg-gray-800/30'}`}
                      onDragOver={e => e.preventDefault()}
                    >
                      <input 
                        type="file" 
                        multiple 
                        accept=".csv"
                        className="absolute inset-0 opacity-0 cursor-pointer"
                        onChange={e => setFiles(Array.from(e.target.files || []))}
                      />
                      <Upload className="mx-auto mb-4 text-gray-500 group-hover:text-blue-400 transition-colors" size={40} />
                      <p className="text-gray-300 font-medium">Click to upload CSVs</p>
                      <p className="text-gray-500 text-xs mt-1">Select one or more sample files</p>
                    </div>
                    {files.length > 0 && (
                      <div className="file-list p-2 bg-gray-800/20 rounded-xl max-h-40 overflow-y-auto border border-gray-800">
                        {files.map(f => (
                          <div key={f.name} className="file-item bg-gray-800/50 border border-gray-700 py-2 px-3">
                            <span className="truncate flex-1 pr-4 text-xs text-gray-300">{f.name}</span>
                            <button onClick={() => setFiles(files.filter(x => x !== f))} className="text-gray-500 hover:text-red-400 transition-colors">
                              <Trash2 size={14} />
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Excel Upload */}
                  <div className="space-y-4">
                    <label className="text-sm font-bold flex items-center gap-2 text-gray-300">
                      <Layout size={18} className="text-purple-400" /> Target Excel Template
                    </label>
                    <div 
                      className={`drop-zone p-8 border-dashed border-2 rounded-2xl transition-all cursor-pointer group relative ${excelFile ? 'border-purple-500/50 bg-purple-500/5' : 'border-gray-800 hover:border-purple-500 bg-gray-800/30'}`}
                    >
                      <input 
                        type="file" 
                        accept=".xlsx"
                        className="absolute inset-0 opacity-0 cursor-pointer"
                        onChange={e => setExcelFile(e.target.files?.[0] || null)}
                      />
                      <FileSpreadsheet className="mx-auto mb-4 text-gray-500 group-hover:text-purple-400 transition-colors" size={40} />
                      <p className="text-gray-300 font-medium">{excelFile ? excelFile.name : 'Click to upload Excel'}</p>
                      <p className="text-gray-500 text-xs mt-1">The master file with your structure</p>
                    </div>
                  </div>
                </div>

                <div className="flex justify-between pt-8 border-t border-gray-800">
                  <button onClick={prevStep} className="btn btn-secondary px-8">
                    <ChevronLeft size={18} /> Back
                  </button>
                  <button 
                    onClick={handleAnalyze}
                    disabled={loading || files.length === 0 || !excelFile}
                    className="btn btn-primary px-10 shadow-lg shadow-blue-500/20"
                  >
                    {loading ? <><div className="spinner mr-2" /> Analyzing...</> : <>Run Analysis <ChevronRight size={18} /></>}
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'sheets' && (
              <div className="space-y-8 fade-in">
                <div>
                  <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <Layers className="text-blue-400 w-6 h-6" /> Target Layout
                  </h2>
                  <p className="text-gray-400 text-sm">Select the sheet and column where your data labels are located.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="space-y-4">
                    <label className="text-sm font-bold text-gray-400">Target Sheet</label>
                    <select 
                      className="select bg-gray-800 border-gray-700 focus:border-blue-500 w-full"
                      value={config.target_sheet}
                      onChange={e => setConfig({ ...config, target_sheet: e.target.value })}
                    >
                      {analysis?.excel_analysis.sheets.map((s: any) => (
                        <option key={s.name} value={s.name}>{s.name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="space-y-4">
                    <label className="text-sm font-bold text-gray-400">Label Column (e.g. B)</label>
                    <input 
                      type="text"
                      className="input bg-gray-800 border-gray-700 focus:border-blue-500 w-full uppercase"
                      value={config.label_column}
                      onChange={e => setConfig({ ...config, label_column: e.target.value.toUpperCase() })}
                    />
                  </div>
                </div>

                <div className="flex justify-between pt-8 border-t border-gray-800">
                  <button onClick={prevStep} className="btn btn-secondary px-8">
                    <ChevronLeft size={18} /> Back
                  </button>
                  <button 
                    onClick={handleDiscoverLabels}
                    disabled={loading}
                    className="btn btn-primary px-10 shadow-lg shadow-blue-500/20"
                  >
                    {loading ? <><div className="spinner mr-2" /> Discovering...</> : <>Analyze Column <ChevronRight size={18} /></>}
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'campaigns' && (
              <div className="space-y-6 fade-in">
                <div>
                  <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <CheckCircle2 className="text-emerald-400 w-6 h-6" /> Campaign Settings
                  </h2>
                  <p className="text-gray-400 text-sm">Where do these campaigns start in <b>{config.target_sheet}</b>?</p>
                </div>
                
                <div className="grid grid-cols-1 gap-4">
                  {config.campaign_mappings.map((mapping, idx) => (
                    <div key={mapping.campaign_name} className="p-5 bg-gray-800/30 rounded-2xl border border-gray-800/50 flex items-center justify-between gap-6 transition-all hover:bg-gray-800/50">
                      <div className="flex-1">
                        <span className="font-bold text-gray-200 block truncate">{mapping.campaign_name}</span>
                        <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold">Source Campaign</span>
                      </div>
                      <div className="w-40">
                        <label className="text-[9px] uppercase font-black text-gray-500 mb-1 block">Start Row</label>
                        <input 
                          type="number"
                          className="input bg-gray-900 border-gray-700 py-2 h-9 text-sm"
                          value={mapping.start_row}
                          onChange={e => {
                              const newMappings = [...config.campaign_mappings];
                              newMappings[idx].start_row = parseInt(e.target.value);
                              setConfig({ ...config, campaign_mappings: newMappings });
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex justify-between pt-8 border-t border-gray-800">
                  <button onClick={prevStep} className="btn btn-secondary px-8">
                    <ChevronLeft size={18} /> Back
                  </button>
                  <button 
                    onClick={nextStep}
                    className="btn btn-primary px-10 shadow-lg shadow-blue-500/20"
                  >
                    Next: Template Mapping <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'templates' && (
              <div className="space-y-6 fade-in">
                 <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gray-800/20 p-6 rounded-2xl border border-gray-800">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                      <Layers className="text-blue-400 w-6 h-6" /> Template Mapping
                    </h2>
                    <p className="text-gray-400 text-sm">Assign each CSV template to the correct row label in Excel.</p>
                  </div>
                  <div className="flex items-center gap-2 bg-gray-900/50 p-2 rounded-xl border border-gray-700 h-fit">
                    <div className="flex flex-col px-2">
                      <span className="text-[10px] uppercase text-gray-500 font-bold">Sheet</span>
                      <select 
                        className="bg-transparent border-none text-xs font-bold text-gray-300 focus:ring-0 p-0 cursor-pointer"
                        value={config.target_sheet}
                        onChange={e => setConfig({ ...config, target_sheet: e.target.value })}
                      >
                        {analysis?.excel_analysis.sheets.map((s: any) => (
                          <option key={s.name} value={s.name}>{s.name}</option>
                        ))}
                      </select>
                    </div>
                    <div className="w-px h-8 bg-gray-700 mx-1" />
                    <div className="flex flex-col px-2">
                      <span className="text-[10px] uppercase text-gray-500 font-bold">Col</span>
                      <input 
                        type="text"
                        className="w-8 bg-transparent border-none p-0 text-center text-xs uppercase font-bold text-blue-400 focus:ring-0"
                        value={config.label_column}
                        onChange={e => setConfig({ ...config, label_column: e.target.value.toUpperCase() })}
                      />
                    </div>
                    <button 
                      onClick={handleDiscoverLabels}
                      disabled={loading}
                      className="ml-2 btn btn-primary py-2 px-3 text-xs gap-1.5 shadow-lg shadow-blue-500/10"
                    >
                      {loading ? <div className="spinner w-3 h-3" /> : <Plus size={14} />}
                      Analyze
                    </button>
                  </div>
                </div>

                <div className="space-y-8">
                  {config.campaign_mappings.map((campaign, cIdx) => {
                    const nextCampaign = config.campaign_mappings[cIdx + 1];
                    const sheetData = analysis?.excel_analysis.sheets.find((s: any) => s.name === config.target_sheet);
                    const allLabels = sheetData?.column_b || [];
                    
                    // Excel First: Show all labels within the campaign row range
                    const campaignLabels = allLabels.filter((l: any) => {
                      return nextCampaign 
                        ? (l.row >= campaign.start_row && l.row < nextCampaign.start_row)
                        : (l.row >= campaign.start_row);
                    });

                    // Dropdown should show templates from CSV that belong to this campaign
                    const campaignCsvTemplates = Array.from(new Set(
                      analysis?.csv_analysis
                        .filter((c: any) => c.campaigns.includes(campaign.campaign_name))
                        .flatMap((c: any) => c.templates)
                    )) as string[];

                    return (

                      <div key={campaign.campaign_name} className="space-y-4">
                        <div className="flex items-center gap-2 py-2 border-b border-gray-800">
                          <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                          <h3 className="font-bold text-gray-400 uppercase tracking-widest text-[10px]">{campaign.campaign_name} Templates</h3>
                        </div>
                        <div className="grid grid-cols-1 gap-2">
                          {campaignLabels.map((label: any) => {
                            // Find if any template is currently mapped to this excel row
                            const currentMapping = config.template_mappings[cIdx]?.templates.find((t: any) => t.excel_row === label.row);
                            const selectedValue = currentMapping?.csv_template_name || "none";

                            return (
                              <div key={label.row} className="flex items-center gap-4 bg-gray-800/20 p-3 rounded-xl border border-gray-800/50 group transition-all hover:bg-gray-800/40 hover:border-blue-500/30">
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm font-semibold truncate text-gray-200">{label.value}</p>
                                  <p className="text-[10px] text-gray-500 uppercase font-bold">Excel Row {label.row}</p>
                                </div>
                                <div className="w-1/2 flex items-center gap-2">
                                  <select 
                                    className={`select py-1.5 h-9 text-xs flex-1 ${selectedValue !== 'none' ? 'bg-blue-900/30 border-blue-500/50 text-blue-200' : 'bg-gray-900 border-gray-700'}`}
                                    value={selectedValue}
                                    onChange={e => {
                                      const val = e.target.value;
                                      const newMappings = [...config.template_mappings];
                                      
                                      if (!newMappings[cIdx]) {
                                        newMappings[cIdx] = { campaign_name: campaign.campaign_name, templates: [] };
                                      }
                                      
                                      newMappings[cIdx].templates = newMappings[cIdx].templates.filter((t: any) => t.excel_row !== label.row);
                                      
                                      if (val !== "none") {
                                        newMappings[cIdx].templates.push({
                                          csv_template_name: val,
                                          excel_row: label.row,
                                          match: true
                                        });
                                      }
                                      setConfig({ ...config, template_mappings: newMappings });
                                    }}
                                  >
                                    <option value="none">Select CSV Template...</option>
                                    {campaignCsvTemplates.map(t => (
                                      <option key={t} value={t}>{t}</option>
                                    ))}
                                  </select>
                                  <button 
                                    onClick={() => {
                                      const match = campaignCsvTemplates.find(t => 
                                        t.toLowerCase().includes(label.value.toLowerCase()) || 
                                        label.value.toLowerCase().includes(t.toLowerCase())
                                      );
                                      if (match) {
                                        const newMappings = [...config.template_mappings];
                                        if (!newMappings[cIdx]) {
                                          newMappings[cIdx] = { campaign_name: campaign.campaign_name, templates: [] };
                                        }
                                        newMappings[cIdx].templates = newMappings[cIdx].templates.filter((t: any) => t.excel_row !== label.row);
                                        newMappings[cIdx].templates.push({
                                          csv_template_name: match,
                                          excel_row: label.row,
                                          match: true
                                        });
                                        setConfig({ ...config, template_mappings: newMappings });
                                      }
                                    }}
                                    className="p-1.5 text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all"
                                    title="Auto-match"
                                  >
                                    <CheckCircle2 size={16} />
                                  </button>
                                </div>
                              </div>
                            );
                          })}
                          {campaignLabels.length === 0 && (
                            <p className="text-xs text-gray-500 italic p-4 text-center">No template labels discovered for this row range ({campaign.start_row}+)</p>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

                <div className="flex justify-between pt-8 border-t border-gray-800">
                  <button onClick={prevStep} className="btn btn-secondary px-8">
                    <ChevronLeft size={18} /> Back
                  </button>
                  <button 
                    onClick={nextStep}
                    className="btn btn-primary px-10 shadow-lg shadow-blue-500/20"
                  >
                    Next: Week Columns <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'weeks' && (
              <div className="space-y-6 fade-in">
                <div>
                  <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <Settings className="text-amber-400 w-6 h-6" /> Week Columns
                  </h2>
                  <p className="text-gray-400 text-sm">Define which column in Excel corresponds to each week.</p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[...Array(8)].map((_, i) => {
                    const weekNum = (i + 1).toString().padStart(2, '0');
                    return (
                      <div key={weekNum} className="space-y-1.5">
                        <label className="text-[10px] uppercase font-bold text-gray-500 px-1">Week {weekNum}</label>
                        <input 
                          type="text" 
                          placeholder="Col (AY)"
                          className="input bg-gray-800 border-gray-700 py-2 text-center uppercase font-mono text-sm"
                          value={config.week_columns.mappings[weekNum] || ''}
                          onChange={e => {
                            const newMappings = { ...config.week_columns.mappings };
                            newMappings[weekNum] = e.target.value.toUpperCase();
                            setConfig({ ...config, week_columns: { ...config.week_columns, mappings: newMappings } });
                          }}
                        />
                      </div>
                    );
                  })}
                </div>

                <div className="flex justify-between pt-8 border-t border-gray-800">
                  <button onClick={prevStep} className="btn btn-secondary px-8">
                    <ChevronLeft size={18} /> Back
                  </button>
                  <button 
                    onClick={nextStep}
                    className="btn btn-primary px-10 shadow-lg shadow-blue-500/20"
                  >
                    Next: Review <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            )}

            {currentStep === 'review' && (
              <div className="space-y-8 fade-in">
                <div className="text-center">
                  <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
                    <CheckCircle2 size={32} className="text-emerald-400" />
                  </div>
                  <h2 className="text-3xl font-bold">Review Configuration</h2>
                  <p className="text-gray-400 mt-2">Almost there! Verify your settings before finalize.</p>
                </div>

                <div className="bg-gray-800/20 rounded-3xl p-8 border border-gray-800 space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
                      <h4 className="text-[9px] uppercase font-black text-gray-500 mb-1">ID</h4>
                      <p className="font-bold text-lg text-blue-400">{config.id}</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
                      <h4 className="text-[9px] uppercase font-black text-gray-500 mb-1">Name</h4>
                      <p className="font-bold text-lg">{config.name}</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
                      <h4 className="text-[9px] uppercase font-black text-gray-500 mb-1">Sheet</h4>
                      <p className="font-bold text-lg text-purple-400">{config.target_sheet}</p>
                    </div>
                  </div>
                </div>

                {status && (
                  <div className={`p-4 rounded-2xl flex items-center gap-3 border ${status.type === 'success' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'}`}>
                    {status.type === 'success' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
                    <span className="font-semibold text-sm">{status.message}</span>
                  </div>
                )}

                <div className="flex justify-between pt-6">
                  <button onClick={prevStep} className="btn btn-secondary px-8">
                    <ChevronLeft size={18} /> Back
                  </button>
                  <div className="flex gap-4">
                    {status?.type === 'success' ? (
                      <Link href="/" className="btn btn-primary px-8 bg-gray-100 text-gray-900 hover:bg-white">
                        Go to Dashboard
                      </Link>
                    ) : (
                      <button 
                        onClick={saveConfig}
                        disabled={loading}
                        className="btn btn-primary px-10 shadow-lg shadow-blue-500/20 bg-gradient-to-r from-blue-600 to-purple-600 border-none"
                      >
                        {loading ? <><div className="spinner mr-2" /> Saving...</> : <><Save size={18} /> Save & Finalize</>}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
