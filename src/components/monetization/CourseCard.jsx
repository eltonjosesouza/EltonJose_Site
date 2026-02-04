import Link from "next/link";
import Image from "next/image";

const CourseCard = ({ title, description, price, image, link, tags = [] }) => {
  return (
    <div className="group flex flex-col items-center justify-between rounded-2xl border border-solid border-dark/25 bg-light p-4 shadow-lg transition-transform duration-300 hover:scale-[1.02] dark:border-light/25 dark:bg-dark border-r-4 border-b-4">
      {/* Image Placeholder */}
      <div className="relative w-full h-48 mb-4 overflow-hidden rounded-xl bg-gray-200 dark:bg-gray-700">
         {/* Ideally use next/image here with a real src */}
         <div className="absolute inset-0 flex items-center justify-center text-4xl text-gray-400">
            {image ? <Image src={image} alt={title} fill className="object-cover" /> : "📚"}
         </div>
      </div>

      <div className="w-full flex flex-col flex-grow">
        <div className="flex flex-wrap gap-2 mb-2">
            {tags.map(tag => (
                <span key={tag} className="text-xs px-2 py-1 bg-accent/20 dark:bg-accentDark/20 text-accent dark:text-accentDark rounded-full font-semibold uppercase">
                    {tag}
                </span>
            ))}
        </div>
        <h3 className="text-xl font-bold capitalize text-dark dark:text-light mb-2">
          <Link href={link} className="hover:underline">
            {title}
          </Link>
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-4 flex-grow">
          {description}
        </p>
      </div>

      <div className="w-full mt-4 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 pt-4">
        <span className="text-lg font-bold text-dark dark:text-light">
          {price === 0 ? "Free" : `$${price}`}
        </span>
        <Link
          href={link}
          className="px-4 py-2 text-sm font-semibold text-light bg-dark rounded-lg dark:text-dark dark:bg-light hover:bg-accent dark:hover:bg-accentDark transition-colors"
        >
          View Course
        </Link>
      </div>
    </div>
  );
};

export default CourseCard;
