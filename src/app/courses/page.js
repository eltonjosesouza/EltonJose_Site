import React from "react";
import CourseCard from "@/src/components/monetization/CourseCard";
import AdBanner from "@/src/components/monetization/AdBanner";
import SupporterCTA from "@/src/components/monetization/SupporterCTA";

const courses = [];

export const metadata = {
  title: "Cursos e Materiais",
  description: "Cursos e materiais exclusivos para acelerar sua carreira como desenvolvedor.",
};

export default function CoursesPage() {
  return (
    <article className="mt-12 flex flex-col text-center">
      <h1 className="text-4xl font-bold capitalize  text-dark dark:text-light">
        Cursos e Materiais
      </h1>
      <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
        Conhecimento direto do campo de batalha. Sem enrolação.
      </p>

      <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-4 md:px-0">
        {courses.length > 0 ? (
          courses.map((course, index) => (
            <CourseCard key={index} {...course} />
          ))
        ) : (
          <div className="col-span-full text-center py-10">
            <p className="text-xl text-gray-500 dark:text-gray-100 font-medium">
              🚀 Em breve novos cursos e materiais exclusivos!
            </p>
            <p className="text-sm text-gray-400 dark:text-gray-300 mt-2">
              Enquanto isso, apoie o trabalho para manter o blog no ar.
            </p>
          </div>
        )}
      </div>

      <div className="mt-24">
         <h2 className="text-2xl font-bold mb-8 text-dark dark:text-light">Apoie meu trabalho</h2>
         <SupporterCTA />
      </div>

       <div className="mt-12">
          <AdBanner placement="article-bottom" />
       </div>
    </article>
  );
}
