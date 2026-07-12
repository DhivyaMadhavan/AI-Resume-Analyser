import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { analyzeResume } from "../services/resumeService";

export default function useResumeAnalysis() {

    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

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

            const result = await analyzeResume(
                file,
                mode,
                jobDescription,
                role
            );
            console.log("====================================");
            console.log("Analysis Source :", result.source);
            console.log("Resume Hash     :", result.resume_hash);
            console.log("====================================");
            
            navigate(`/dashboard/${result.resume_hash}`);

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
