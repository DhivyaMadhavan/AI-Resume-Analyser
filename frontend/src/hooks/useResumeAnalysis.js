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
            setError("Please upload a resume.");
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

            navigate("/dashboard", {
                state: result,
            });

        }
        catch (err) {

            if (err.response) {

                setError(
                    err.response.data.detail
                );

            }
            else {

                setError(
                    "Unable to connect to server."
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