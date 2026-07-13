import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { 
    analyzeResume,
    getJobStatus
} from "../services/resumeService";

export default function useResumeAnalysis() {

    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const waitForJobCompletion = async(jobId)=>{

        while(true){

            const job = await getJobStatus(jobId);


            console.log(
                "JOB STATUS:",
                job.status
            );


            if(job.status === "completed"){

                return job.result;

            }


            if(job.status === "failed"){

                throw new Error(
                    job.error || "Analysis failed"
                );

            }


            await new Promise(
                resolve => setTimeout(resolve,2000)
            );

        }

    };

    const analyze = async ({
        file,
        mode,
        jobDescription,
        role,
    }) => {

        setError("");

        // Resume validation
        if (!file) {
            setError("Please upload a valid PDF resume.");
            return;
        }

        // JD validation
        if (
            mode === "jd" &&
            !jobDescription.trim()
        ) {
            setError("Please enter a Job Description.");
            return;
        }

        // Role validation
        if (
            mode === "role" &&
            !role
        ) {
            setError("Please select a role.");
            return;
        }

        try {

            setLoading(true);

            const uploadResponse = await analyzeResume(
                file,
                mode,
                jobDescription,
                role
            );


            console.log(
                "JOB CREATED:",
                uploadResponse.job_id
            );



            const result = await waitForJobCompletion(
                uploadResponse.job_id
            );

            console.log("========== Resume Analysis ==========");
            console.log("Resume Source :", result.source);
            console.log("Resume Hash   :", result.resume_hash);
            
            if (result.matching) {
                console.log("========== Matching ==========");
                console.log("Mode          :", result.matching.mode);
                console.log("Match Source  :", result.matching.metadata?.source);
            }

            console.log("====================================");
            
            navigate(`/dashboard/${result.resume_hash}`, {
                state: {
                    mode: mode,
                    analysisResult: result
                },
            });

        }
        catch (err) {
            console.error("UPLOAD ERROR:", err);
            console.error("RESPONSE:", err.response);

            if (!err.response) {

                setError(
                    "Server is unavailable. Please try again later."
                );

            }
            else if (err.response.status === 400) {

                setError(
                    "Please upload a valid PDF resume."
                );

            }
            else if (err.response.status === 500) {

                setError(
                    "AI analysis failed. Please retry."
                );

            }
            else {

                setError(
                    "Something went wrong. Please try again."
                );

            }
        }
        finally {

            setLoading(false);

        }

    };

    return {

        analyze,

        loading,

        error,

    };

}
