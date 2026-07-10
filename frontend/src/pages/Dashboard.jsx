import { useLocation } from "react-router-dom";

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

const Dashboard = () => {
  const location = useLocation();

  const analysis = location.state?.analysis;
  const mode = location.state?.mode;

  console.log("Dashboard State:", location.state);
  console.log("Analysis:", analysis);
  
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">
        AI Resume Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <ATSCard analysis={analysis} />
        <SummaryCard analysis={analysis} />

        <PersonalInfoCard analysis={analysis} />

        <ExperienceCard analysis={analysis} />

        <SkillsCard analysis={analysis} />

        <StrengthsCard analysis={analysis} />

        <WeaknessesCard analysis={analysis} />

        <RecommendationCard analysis={analysis} />
 
        {mode === "jd" && <JDMatchCard />}

        {mode === "role" && <RoleMatchCard />}

      </div>
    </div>
  );
};

export default Dashboard;