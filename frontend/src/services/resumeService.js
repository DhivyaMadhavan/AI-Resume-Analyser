import api from "./api";

export async function analyzeResume(
    file,
    mode,
    jobDescription,
    role
){

    const formData=new FormData();

    formData.append("file",file);

    formData.append("mode",mode);

    if(mode==="jd"){

        formData.append(
            "job_description",
            jobDescription
        );

    }

    if(mode==="role"){

        formData.append(
            "role",
            role
        );

    }

    const response=await api.post(

        "/api/v1/resume/upload",

        formData

    );

    return response.data;

}