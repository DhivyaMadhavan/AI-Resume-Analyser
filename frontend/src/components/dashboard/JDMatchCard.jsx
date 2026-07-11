const JDMatchCard = ({ matching }) => {   
  const result = matching?.result;

  if (!result) {
    return null;
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">

      <h2 className="text-xl font-semibold mb-5">
        🎯 Job Description Match
      </h2>


      {/* Match Score */}
      <div className="flex items-center justify-center mb-6">

        <div className="w-28 h-28 rounded-full border-8 border-blue-500 flex items-center justify-center">

          <span className="text-3xl font-bold text-blue-600">
            {result.match_score}%
          </span>

        </div>

      </div>


      {/* Matched Skills */}
      <div className="mb-5">

        <h3 className="font-semibold text-green-600 mb-2">
          ✅ Matching Skills
        </h3>

        <div className="flex flex-wrap gap-2">

          {result.matched_skills?.map((skill,index)=>(
            <span
              key={index}
              className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
            >
              {skill}
            </span>
          ))}

        </div>

      </div>



      {/* Missing Skills */}
      <div className="mb-5">

        <h3 className="font-semibold text-red-600 mb-2">
          ⚠ Missing Skills
        </h3>


        <div className="flex flex-wrap gap-2">

          {result.missing_skills?.map((skill,index)=>(
            <span
              key={index}
              className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
            >
              {skill}
            </span>
          ))}

        </div>

      </div>



      {/* Strengths */}

      <div className="mb-5">

        <h3 className="font-semibold mb-2">
          💪 Strengths
        </h3>


        <ul className="list-disc ml-5 text-gray-700 space-y-1">

          {result.strengths?.slice(0,4).map((item,index)=>(
            <li key={index}>
              {item}
            </li>
          ))}

        </ul>

      </div>



      {/* Recommendations */}

      <div>

        <h3 className="font-semibold mb-2">
          🚀 Recommendations
        </h3>


        <ul className="list-disc ml-5 text-gray-700 space-y-1">

          {result.tailored_recommendations?.slice(0,4).map((item,index)=>(
            <li key={index}>
              {item}
            </li>
          ))}

        </ul>

      </div>


    </div>
  );
};


export default JDMatchCard;