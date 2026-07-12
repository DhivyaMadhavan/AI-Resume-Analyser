import Loader from "../components/Loader";
import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

import ATSCard from "../components/dashboard/ATSCard";
import SummaryCard from "../components/dashboard/SummaryCard";
import PersonalInfoCard from "../components/dashboard/PersonalInfoCard";
import ExperienceCard from "../components/dashboard/ExperienceCard";
import SkillsCard from "../components/dashboard/SkillsCard";
import StrengthsCard from "../components/dashboard/StrengthsCard";
import WeaknessesCard from "../components/dashboard/WeaknessesCard";
import RecommendationCard from "../components/dashboard/RecommendationCard";
import JDMatchCard from "../components/dashboard/JDMatchCard";
import RoleMatchCard from "../components/dashboard/RoleMatchCard";
import AnalysisInfo from "../components/dashboard/AnalysisInfo";

import { generatePDFReport } from "../utils/reportGenerator";

const Dashboard = () => {
  const { resume_hash } = useParams();

  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/api/v1/resume/${resume_hash}`
        );

        

        setResumeData(response.data);
      } catch (err) {
        console.error(err);
        setError("Unable to load resume analysis.");
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [resume_hash]);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-600">
        {error}
      </div>
    );
  }

  const analysis = resumeData?.analysis;
  const matching = resumeData?.matching;
  console.log("resumeData:", resumeData);
  console.log("matching:", matching);
  console.log("matching.mode:", matching?.mode);
  console.log("matching.result:", matching?.result);

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-gray-800 text-[13px] leading-relaxed">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            AI Resume Dashboard
          </h1>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => generatePDFReport(resumeData)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-xs font-medium shadow-sm transition"
          >
            Download Report
          </button>

          <button
            onClick={() => navigate("/")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-xs font-medium shadow-sm transition"
          >
            Upload Another
          </button>
        </div>
      </div>

      {/* Processing Information */}
      <AnalysisInfo resumeData={resumeData} />

      {/* Dashboard Cards */}
      <div className="columns-1 md:columns-2 gap-6 space-y-6">

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <ATSCard analysis={analysis} />
        </div>

        {matching?.mode && (
          <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
            <div className="break-inside-avoid bg-yellow-100 p-5 rounded-xl">
              <p>Mode: {String(matching?.mode)}</p>
              <p>Has Result: {String(!!matching?.result)}</p>
  
              {matching.mode === "jd" && (
                <JDMatchCard matching={matching} />
              )}
  
              {matching.mode === "role" && (
                <RoleMatchCard matching={matching} />
           
            )}
              </div>
          </div>
        )}

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <SummaryCard analysis={analysis} />
        </div>

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <PersonalInfoCard analysis={analysis} />
        </div>

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <ExperienceCard analysis={analysis} />
        </div>

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <SkillsCard analysis={analysis} />
        </div>

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <StrengthsCard analysis={analysis} />
        </div>

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <WeaknessesCard analysis={analysis} />
        </div>

        <div className="break-inside-avoid bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <RecommendationCard analysis={analysis} />
        </div>

      </div>

    </div>
  );
};

export default Dashboard;
