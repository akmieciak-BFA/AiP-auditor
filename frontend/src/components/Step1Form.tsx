import { useState } from 'react';
import { Loader, FileText } from 'lucide-react';
import { step1API } from '../services/api';
import type { Step1Result } from '../types';

interface Step1FormProps {
  projectId: number;
  onComplete: () => void;
}

export default function Step1Form({ projectId, onComplete }: Step1FormProps) {
  const [currentSection, setCurrentSection] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<Step1Result | null>(null);

  // SEKCJA A: INFORMACJE ORGANIZACYJNE
  const [formData, setFormData] = useState({
    // Q1: Podstawowe dane organizacji
    organization_name: '',
    industry: 'Manufacturing',
    company_size: 'Mikro (1-9)',
    annual_revenue: 0,
    headquarters_location: '',
    number_of_locations: 1,
    
    // Q2: Struktura operacyjna
    functional_areas: [] as string[],
    critical_areas: [] as string[],
    
    // Q3: Poziom cyfryzacji (0-10)
    digital_maturity_erp: 0,
    digital_maturity_crm: 0,
    digital_maturity_production: 0,
    digital_maturity_rpa: 0,
    digital_maturity_analytics: 0,
    digital_maturity_iot: 0,
    digital_maturity_ai: 0,
    digital_maturity_communication: 0,
    digital_maturity_workflow: 0,
    digital_maturity_cloud: 0,
    
    // Q4: Systemy IT
    it_systems: {} as Record<string, string>,
    systems_integrated: 'Częściowo',
    
    // Q5: Budżet
    budget_range: '50 000 - 150 000 PLN',
    budget_sources: [] as string[],
    expected_payback_months: 12,
    
    // SEKCJA B: PROBLEMY I WĄSKIE GARDŁA
    main_challenges_ranked: [] as string[],
    challenges_description: '',
    time_consuming_processes: {} as Record<string, number>,
    error_prone_processes: {} as Record<string, any>,
    bottlenecks: {} as Record<string, any>,
    process_maturity: {} as Record<string, any>,
    
    // SEKCJA C: CELE I OCZEKIWANIA
    automation_goals_ranked: [] as string[],
    automation_goals_weights: {} as Record<string, number>,
    expected_cost_reduction_percent: 0,
    expected_revenue_increase_percent: 0,
    expected_roi_percent: 0,
    acceptable_payback_months: 12,
    specific_savings_goal: 0,
    savings_sources_description: '',
    operational_targets: {} as Record<string, number>,
    employee_expectations: {} as Record<string, any>,
    change_management_readiness: 'Częściowo',
    
    // Timeline
    preferred_start_date: '',
    preferred_phase1_end_date: '',
    phased_approach: 'Tak',
    number_of_phases: 3,
    preferred_approach: 'Hybrydowe',
    business_deadlines: '',
    
    // SEKCJA D: ZASOBY I OGRANICZENIA
    has_it_team: 'Tak',
    it_team_size: 0,
    has_bpm_department: 'Nie',
    bpm_team_size: 0,
    automation_experience: 'Ograniczone',
    has_project_manager: 'Tak',
    has_change_manager: 'Nie',
    stakeholder_availability: 'Częściowa',
    constraints_and_risks: {} as Record<string, number>,
    special_requirements: [] as string[],
    
    // SEKCJA E: KONTEKST STRATEGICZNY
    business_strategy_description: '',
    strategic_initiatives: [] as string[],
    additional_notes: '',
  });

  const functionalAreasOptions = [
    'Produkcja / Manufacturing',
    'Logistyka i magazynowanie',
    'Sprzedaż i obsługa klienta',
    'Marketing',
    'Finanse i księgowość',
    'HR i zarządzanie personelem',
    'IT i wsparcie techniczne',
    'Zakupy i procurement',
    'Kontrola jakości / QA',
    'R&D / Innowacje',
    'Zarządzanie projektami',
    'Administracja i back-office',
  ];

  const challengesOptions = [
    'Wysokie koszty operacyjne',
    'Niska produktywność pracowników',
    'Długie czasy realizacji procesów',
    'Błędy i niska jakość',
    'Problemy z przepustowością / capacity',
    'Brak widoczności procesów / danych',
    'Słaba obsługa klienta',
    'Problemy z compliance / zgodnością',
    'Wysokie koszty utrzymania systemów IT',
    'Trudności w skalowaniu działalności',
    'Rotacja pracowników / problemy kadrowe',
    'Brak innowacyjności / konkurencyjności',
  ];

  const automationGoalsOptions = [
    'Redukcja kosztów operacyjnych',
    'Zwiększenie produktywności',
    'Poprawa jakości i redukcja błędów',
    'Skrócenie czasu realizacji procesów',
    'Lepsza obsługa klienta',
    'Zwiększenie skalowalności biznesu',
    'Poprawa compliance i bezpieczeństwa',
    'Zwiększenie konkurencyjności / innowacyjności',
  ];

  const handleCheckboxGroup = (field: string, option: string) => {
    const current = formData[field as keyof typeof formData] as string[];
    if (current.includes(option)) {
      setFormData({ ...formData, [field]: current.filter(v => v !== option) });
    } else {
      setFormData({ ...formData, [field]: [...current, option] });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setError('');

    try {
      const result = await step1API.analyze(projectId, {
        organization_data: formData as any,
        questionnaire_answers: {},
        processes_list: [],
      });
      setResults(result);
      setTimeout(() => onComplete(), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd analizy');
    } finally {
      setIsAnalyzing(false);
    }
  };

  if (results) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white mb-4">✓ Analiza zakończona</h2>
        <div className="bg-primary-500/10 border border-primary-500 p-4 rounded-lg">
          <p className="text-primary-500">Raport został wygenerowany. Przejście do Kroku 2...</p>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <div className="bg-dark-800 p-6 rounded-lg">
        <h2 className="text-2xl font-bold text-white mb-2">
          Krok 1: Formularz Początkowy - Audyt Automatyzacyjny BFA
        </h2>
        <p className="text-gray-400 mb-6">
          Formularz stanowi punkt wejścia do audytu automatyzacyjnego BFA. Na podstawie 20 pytań, 
          Claude API z extended thinking zidentyfikuje TOP 3-5-10 procesów o największym potencjale automatyzacji.
        </p>
      </div>

      {/* Section Navigation */}
      <div className="flex space-x-2 overflow-x-auto">
        {[
          { num: 1, name: 'Organizacja' },
          { num: 2, name: 'Problemy' },
          { num: 3, name: 'Cele' },
          { num: 4, name: 'Zasoby' },
          { num: 5, name: 'Strategia' },
        ].map(section => (
          <button
            key={section.num}
            type="button"
            onClick={() => setCurrentSection(section.num)}
            className={`px-4 py-2 rounded-lg whitespace-nowrap ${
              currentSection === section.num
                ? 'bg-primary-500 text-white'
                : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
            }`}
          >
            {section.name}
          </button>
        ))}
      </div>

      {/* SEKCJA A: INFORMACJE ORGANIZACYJNE */}
      {currentSection === 1 && (
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-primary-500">
            SEKCJA A: INFORMACJE ORGANIZACYJNE (Pytania 1-5)
          </h3>

          {/* Pytanie 1: Podstawowe dane */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">Pytanie 1: Podstawowe dane organizacji</h4>
            
            <div>
              <label className="label">Nazwa organizacji *</label>
              <input
                type="text"
                value={formData.organization_name}
                onChange={(e) => setFormData({ ...formData, organization_name: e.target.value })}
                className="input"
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Branża *</label>
                <select
                  value={formData.industry}
                  onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  className="input"
                  required
                >
                  <option>Manufacturing (Produkcja)</option>
                  <option>Financial Services (Usługi finansowe)</option>
                  <option>Healthcare (Ochrona zdrowia)</option>
                  <option>Retail (Handel detaliczny)</option>
                  <option>Logistics & Supply Chain (Logistyka)</option>
                  <option>Energy & Utilities (Energia)</option>
                  <option>IT & Technology</option>
                  <option>Professional Services</option>
                  <option>Public Sector (Sektor publiczny)</option>
                </select>
              </div>

              <div>
                <label className="label">Wielkość organizacji *</label>
                <select
                  value={formData.company_size}
                  onChange={(e) => setFormData({ ...formData, company_size: e.target.value })}
                  className="input"
                  required
                >
                  <option>Mikro (1-9 pracowników)</option>
                  <option>Mała (10-49 pracowników)</option>
                  <option>Średnia (50-249 pracowników)</option>
                  <option>Duża (250-999 pracowników)</option>
                  <option>Bardzo duża (1000+ pracowników)</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="label">Roczny obrót (PLN)</label>
                <input
                  type="number"
                  value={formData.annual_revenue}
                  onChange={(e) => setFormData({ ...formData, annual_revenue: parseFloat(e.target.value) })}
                  className="input"
                />
              </div>

              <div>
                <label className="label">Lokalizacja głównej siedziby *</label>
                <input
                  type="text"
                  value={formData.headquarters_location}
                  onChange={(e) => setFormData({ ...formData, headquarters_location: e.target.value })}
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label">Liczba lokalizacji/oddziałów *</label>
                <input
                  type="number"
                  value={formData.number_of_locations}
                  onChange={(e) => setFormData({ ...formData, number_of_locations: parseInt(e.target.value) })}
                  className="input"
                  min="1"
                  required
                />
              </div>
            </div>
          </div>

          {/* Pytanie 2: Struktura operacyjna */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">Pytanie 2: Struktura operacyjna</h4>
            <p className="text-sm text-gray-400">Zaznacz wszystkie aktywne obszary funkcjonalne (wymagane minimum 3)</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {functionalAreasOptions.map(area => (
                <label key={area} className="flex items-center space-x-2 p-2 bg-dark-700 rounded cursor-pointer hover:bg-dark-600">
                  <input
                    type="checkbox"
                    checked={formData.functional_areas.includes(area)}
                    onChange={() => handleCheckboxGroup('functional_areas', area)}
                    className="w-4 h-4"
                  />
                  <span className="text-white text-sm">{area}</span>
                </label>
              ))}
            </div>

            <div>
              <label className="label">Wskaż 3 najbardziej krytyczne obszary *</label>
              <p className="text-xs text-gray-500 mb-2">Wybierz dokładnie 3 obszary</p>
              <div className="space-y-1">
                {formData.functional_areas.map(area => (
                  <label key={area} className="flex items-center space-x-2 p-2 bg-dark-700 rounded cursor-pointer hover:bg-dark-600">
                    <input
                      type="checkbox"
                      checked={formData.critical_areas.includes(area)}
                      onChange={() => handleCheckboxGroup('critical_areas', area)}
                      disabled={!formData.critical_areas.includes(area) && formData.critical_areas.length >= 3}
                      className="w-4 h-4"
                    />
                    <span className="text-white text-sm">{area}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Pytanie 3: Poziom cyfryzacji */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">
              Pytanie 3: Obecny poziom cyfryzacji i automatyzacji
            </h4>
            <p className="text-sm text-gray-400">
              Oceń obecny poziom (0 = brak, 10 = pełna automatyzacja)
            </p>

            {[
              { key: 'digital_maturity_erp', label: 'Systemy ERP/zarządzania zasobami' },
              { key: 'digital_maturity_crm', label: 'CRM / zarządzanie relacjami z klientami' },
              { key: 'digital_maturity_production', label: 'Automatyzacja procesów produkcyjnych' },
              { key: 'digital_maturity_rpa', label: 'Automatyzacja procesów biurowych (RPA)' },
              { key: 'digital_maturity_analytics', label: 'Analityka danych i Business Intelligence' },
              { key: 'digital_maturity_iot', label: 'IoT / czujniki i monitoring' },
              { key: 'digital_maturity_ai', label: 'AI/ML w procesach decyzyjnych' },
              { key: 'digital_maturity_communication', label: 'Automatyzacja komunikacji (chatboty, email)' },
              { key: 'digital_maturity_workflow', label: 'Workflow automation / BPM' },
              { key: 'digital_maturity_cloud', label: 'Cloud computing i infrastruktura' },
            ].map(item => (
              <div key={item.key}>
                <label className="label">{item.label}</label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="0"
                    max="10"
                    value={formData[item.key as keyof typeof formData]}
                    onChange={(e) => setFormData({ ...formData, [item.key]: parseInt(e.target.value) })}
                    className="flex-1"
                  />
                  <span className="text-primary-500 font-bold w-8 text-center">
                    {formData[item.key as keyof typeof formData]}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Pytanie 5: Budżet */}
          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">Pytanie 5: Budżet i gotowość inwestycyjna</h4>
            
            <div>
              <label className="label">Planowany budżet na automatyzację (12 miesięcy) *</label>
              <select
                value={formData.budget_range}
                onChange={(e) => setFormData({ ...formData, budget_range: e.target.value })}
                className="input"
                required
              >
                <option>Poniżej 50 000 PLN</option>
                <option>50 000 - 150 000 PLN</option>
                <option>150 000 - 500 000 PLN</option>
                <option>500 000 - 1 000 000 PLN</option>
                <option>1 000 000 - 3 000 000 PLN</option>
                <option>Powyżej 3 000 000 PLN</option>
                <option>Budżet nie został jeszcze określony</option>
              </select>
            </div>

            <div>
              <label className="label">Oczekiwany okres zwrotu (payback period) *</label>
              <select
                value={formData.expected_payback_months}
                onChange={(e) => setFormData({ ...formData, expected_payback_months: parseInt(e.target.value) })}
                className="input"
                required
              >
                <option value="6">Do 6 miesięcy</option>
                <option value="12">6-12 miesięcy</option>
                <option value="24">12-24 miesiące</option>
                <option value="36">24-36 miesięcy</option>
                <option value="48">Powyżej 36 miesięcy</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="button"
              onClick={() => setCurrentSection(2)}
              className="btn btn-primary"
            >
              Następna sekcja →
            </button>
          </div>
        </div>
      )}

      {/* SEKCJA B: PROBLEMY (simplified for brevity) */}
      {currentSection === 2 && (
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-primary-500">
            SEKCJA B: IDENTYFIKACJA PROBLEMÓW I WĄSKICH GARDEŁ (Pytania 6-10)
          </h3>

          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">Pytanie 6: Główne wyzwania operacyjne</h4>
            <p className="text-sm text-gray-400">Opisz szczegółowo TOP 3 wyzwania</p>
            <textarea
              value={formData.challenges_description}
              onChange={(e) => setFormData({ ...formData, challenges_description: e.target.value })}
              className="input"
              rows={6}
              placeholder="Opisz najważniejsze wyzwania operacyjne w Twojej organizacji..."
              required
            />
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setCurrentSection(1)}
              className="btn btn-secondary"
            >
              ← Poprzednia sekcja
            </button>
            <button
              type="button"
              onClick={() => setCurrentSection(3)}
              className="btn btn-primary"
            >
              Następna sekcja →
            </button>
          </div>
        </div>
      )}

      {/* SEKCJA C: CELE */}
      {currentSection === 3 && (
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-primary-500">
            SEKCJA C: CELE I OCZEKIWANIA (Pytania 11-15)
          </h3>

          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">Pytanie 12: Oczekiwane korzyści finansowe</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Oczekiwana redukcja kosztów operacyjnych (%/rok)</label>
                <input
                  type="number"
                  value={formData.expected_cost_reduction_percent}
                  onChange={(e) => setFormData({ ...formData, expected_cost_reduction_percent: parseFloat(e.target.value) })}
                  className="input"
                  min="0"
                  max="100"
                />
              </div>

              <div>
                <label className="label">Oczekiwany ROI (%)</label>
                <input
                  type="number"
                  value={formData.expected_roi_percent}
                  onChange={(e) => setFormData({ ...formData, expected_roi_percent: parseFloat(e.target.value) })}
                  className="input"
                  min="0"
                />
              </div>
            </div>

            <div>
              <label className="label">Główne źródła oczekiwanych oszczędności</label>
              <textarea
                value={formData.savings_sources_description}
                onChange={(e) => setFormData({ ...formData, savings_sources_description: e.target.value })}
                className="input"
                rows={3}
                placeholder="np. Redukcja czasu pracy, mniej błędów, niższe koszty materiałów..."
              />
            </div>
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setCurrentSection(2)}
              className="btn btn-secondary"
            >
              ← Poprzednia sekcja
            </button>
            <button
              type="button"
              onClick={() => setCurrentSection(4)}
              className="btn btn-primary"
            >
              Następna sekcja →
            </button>
          </div>
        </div>
      )}

      {/* SEKCJA D: ZASOBY */}
      {currentSection === 4 && (
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-primary-500">
            SEKCJA D: ZASOBY I OGRANICZENIA (Pytania 16-18)
          </h3>

          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">Pytanie 16: Zasoby wewnętrzne</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Czy macie dedykowany zespół IT? *</label>
                <select
                  value={formData.has_it_team}
                  onChange={(e) => setFormData({ ...formData, has_it_team: e.target.value })}
                  className="input"
                  required
                >
                  <option>Tak</option>
                  <option>Nie</option>
                  <option>Częściowo</option>
                </select>
              </div>

              {formData.has_it_team === 'Tak' && (
                <div>
                  <label className="label">Liczba osób w zespole IT</label>
                  <input
                    type="number"
                    value={formData.it_team_size}
                    onChange={(e) => setFormData({ ...formData, it_team_size: parseInt(e.target.value) })}
                    className="input"
                    min="0"
                  />
                </div>
              )}
            </div>

            <div>
              <label className="label">Doświadczenie z projektami automatyzacji *</label>
              <select
                value={formData.automation_experience}
                onChange={(e) => setFormData({ ...formData, automation_experience: e.target.value })}
                className="input"
                required
              >
                <option>Tak, znaczne</option>
                <option>Tak, ograniczone</option>
                <option>Nie</option>
              </select>
            </div>
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setCurrentSection(3)}
              className="btn btn-secondary"
            >
              ← Poprzednia sekcja
            </button>
            <button
              type="button"
              onClick={() => setCurrentSection(5)}
              className="btn btn-primary"
            >
              Następna sekcja →
            </button>
          </div>
        </div>
      )}

      {/* SEKCJA E: STRATEGIA */}
      {currentSection === 5 && (
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-primary-500">
            SEKCJA E: KONTEKST STRATEGICZNY (Pytania 19-20)
          </h3>

          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">
              Pytanie 19: Strategia biznesowa i wizja
            </h4>
            
            <div>
              <label className="label">
                Jaka jest strategia biznesowa organizacji na najbliższe 3-5 lat? *
              </label>
              <textarea
                value={formData.business_strategy_description}
                onChange={(e) => setFormData({ ...formData, business_strategy_description: e.target.value })}
                className="input"
                rows={6}
                placeholder="Opisz główne cele strategiczne, planowane kierunki rozwoju..."
                required
              />
            </div>
          </div>

          <div className="bg-dark-800 p-6 rounded-lg space-y-4">
            <h4 className="text-lg font-semibold text-white">
              Pytanie 20: Dodatkowe informacje i uwagi
            </h4>
            
            <div>
              <label className="label">
                Czy są jakieś dodatkowe informacje, które powinniśmy wziąć pod uwagę?
              </label>
              <textarea
                value={formData.additional_notes}
                onChange={(e) => setFormData({ ...formData, additional_notes: e.target.value })}
                className="input"
                rows={6}
                placeholder="Specyfika branżowa, unikalne wyzwania, wcześniejsze doświadczenia..."
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-2 rounded-lg">
              {error}
            </div>
          )}

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => setCurrentSection(4)}
              className="btn btn-secondary"
            >
              ← Poprzednia sekcja
            </button>
            <button
              type="submit"
              disabled={isAnalyzing}
              className="btn btn-primary flex items-center space-x-2"
            >
              {isAnalyzing ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  <span>Analizowanie z Extended Thinking...</span>
                </>
              ) : (
                <>
                  <FileText className="w-5 h-5" />
                  <span>Zakończ i Analizuj</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </form>
  );
}
