// src/utils/reportGenerator.js

import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";


const PAGE_HEIGHT = 297;
const PAGE_WIDTH = 210;
const MARGIN = 14;



export const generatePDFReport = (resumeData) => {

  if (!resumeData) return;


  const doc = new jsPDF();


  const analysis = resumeData.analysis || {};
  const candidate = analysis.candidate || {};
  const personal = analysis.personal_details || {};

  const matching = resumeData.matching || {};
  const matchResult = matching.result || {};



  let y = 20;



  addHeader(doc);


  y = 35;



  /*
      TITLE
  */

  doc.setFontSize(20);
  doc.setFont("helvetica","bold");

  doc.text(
    "AI Resume Analysis Report",
    MARGIN,
    y
  );


  y += 8;


  doc.setFontSize(10);
  doc.setFont("helvetica","normal");

  doc.text(
    `Generated: ${new Date().toLocaleString()}`,
    MARGIN,
    y
  );


  y += 15;




  /*
      CANDIDATE INFORMATION
  */


  y = addSectionTitle(
    doc,
    "Candidate Information",
    y
  );



  autoTable(doc,{

    startY:y,

    theme:"grid",

    head:[
      [
        "Field",
        "Details"
      ]
    ],

    body:[

      [
        "Name",
        candidate.name || "-"
      ],

      [
        "Email",
        personal.email || "-"
      ],

      [
        "Phone",
        personal.phone || "-"
      ],

      [
        "ATS Score",
        analysis.ats.overall_score ?? "-"
      ]

      

    ]

  });



  y =
  doc.lastAutoTable.finalY + 12;





  /*
      SUMMARY
  */


  y = addSectionTitle(
    doc,
    "Professional Summary",
    y
  );


  y = addParagraph(
    doc,
    candidate.summary || "-",
    y
  );





  /*
      SKILLS
  */


  y = addSectionTitle(
    doc,
    "Technical Skills",
    y
  );


  y = addBulletList(
    doc,
    analysis.skills || [],
    y
  );





  /*
      STRENGTHS
  */


  const strengths = [

    ...(analysis.strengths || []),

    ...(matchResult.strengths || [])

  ];



  y = addSectionTitle(
    doc,
    "Strengths",
    y
  );


  y = addBulletList(
    doc,
    strengths,
    y
  );






  /*
      IMPROVEMENTS
  */


  const improvements = [

    ...(analysis.improvements || []),

    ...(matchResult.weaknesses || [])

  ];



  y = addSectionTitle(
    doc,
    "Areas of Improvement",
    y
  );


  y = addBulletList(
    doc,
    improvements,
    y
  );






  /*
      RECOMMENDATIONS
  */


  const recommendations = [

    ...(analysis.recommendations || []),

    ...(matchResult.tailored_recommendations || [])

  ];



  y = addSectionTitle(
    doc,
    "Recommendations",
    y
  );


  y = addBulletList(
    doc,
    recommendations,
    y
  );






  /*
      JOB MATCHING
  */


  if(matching.mode){


    y = addSectionTitle(
      doc,
      "Job Matching Analysis",
      y
    );



    autoTable(doc,{

      startY:y,

      theme:"grid",

      head:[

        [
          "Field",
          "Details"
        ]

      ],


      body:[


        [
          "Mode",
          matching.mode
        ],


        [
          "Match Score",
          matchResult.match_score ?? "-"
        ],


        [
          "Matched Skills",
          (matchResult.matched_skills || []).join(", ")
        ],


        [
          "Missing Skills",
          (matchResult.missing_skills || []).join(", ")
        ],


        [
          "Interview Readiness",
          matchResult.interview_readiness || "-"
        ]

      ]

    });


  }



  addFooter(doc);



  doc.save(
    "AI_Resume_Report.pdf"
  );

};







function addSectionTitle(doc,title,y){


  y = checkPage(
    doc,
    y,
    35
  );


  doc.setFontSize(14);

  doc.setFont(
    "helvetica",
    "bold"
  );


  doc.text(
    title,
    MARGIN,
    y
  );


  return y + 8;

}






function addParagraph(doc,text,y){


  doc.setFontSize(11);


  const lines =
    doc.splitTextToSize(
      text,
      180
    );



  y = checkPage(
    doc,
    y,
    lines.length * 5
  );


  doc.text(
    lines,
    MARGIN,
    y
  );


  return y +
    lines.length * 5 + 8;

}








function addBulletList(doc,items,y){


  if(!items.length)
    return y;



  items.forEach(item=>{


    const lines =
      doc.splitTextToSize(
        item,
        170
      );


    y = checkPage(
      doc,
      y,
      lines.length * 5 + 5
    );



    doc.text(
      "•",
      MARGIN,
      y
    );


    doc.text(
      lines,
      MARGIN + 5,
      y
    );


    y +=
      lines.length * 5 + 4;


  });



  return y + 5;

}








function checkPage(doc,y,requiredSpace=10){


  if(
    y + requiredSpace > PAGE_HEIGHT - 20
  ){

    doc.addPage();

    addHeader(doc);

    return 35;

  }


  return y;

}








function addHeader(doc){


  doc.setFontSize(9);


  doc.text(
    "AI Resume Analyzer",
    MARGIN,
    10
  );

}








function addFooter(doc){


  const pages =
    doc.getNumberOfPages();



  for(
    let i=1;
    i<=pages;
    i++
  ){

    doc.setPage(i);


    doc.setFontSize(9);


    doc.text(
      `Page ${i} of ${pages}`,
      PAGE_WIDTH - 40,
      PAGE_HEIGHT - 10
    );

  }

}