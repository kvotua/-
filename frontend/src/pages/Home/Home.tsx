import React from "react";
import { Link } from "react-router-dom";
import { EffectCoverflow, Pagination } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";

import { ProjectCard } from "src/entities/ProjectCard/ProjectCard";
import Gallery from "src/assets/gallery.svg?react";
import { useGetProjectsByUserIdQuery } from "src/app/store/slice/ProjectsSlice/projectsApi";
import { SkeletonProjectCard } from "src/entities/ProjectCard/SkeletonProjectCard";
import { ErrorPopup } from "src/shared/ErrorPopup/ErrorPopup";

const Home: React.FC = () => {
  const { data: projects, isLoading, error } = useGetProjectsByUserIdQuery(0);
  return (
    <div className="pt-[4vh] min-h-[100dvh]">
      <div className=" max-w-[430px] mx-auto">
        <h1 className="title">Мои проекты</h1>
        {error ? (
          <ErrorPopup
            errorMessage={"Ой! Произошла ощибка."}
            handleClick={() => console.log(123)}
          />
        ) : (
          <Swiper
            effect={"coverflow"}
            grabCursor={true}
            centeredSlides={true}
            slidesPerView={1.2}
            coverflowEffect={{
              rotate: 50,
              stretch: 0,
              depth: 100,
              modifier: 1,
              slideShadows: false,
            }}
            modules={[EffectCoverflow, Pagination]}
            pagination={true}
            className="h-full pt-[4dvh]"
          >
            {isLoading
              ? [...Array(8)].map((_, i) => (
                  <SwiperSlide key={i}>
                    <SkeletonProjectCard />
                  </SwiperSlide>
                ))
              : projects?.map((project) => (
                  <SwiperSlide key={project.id}>
                    <ProjectCard title={project.name} id={project.id!} />
                  </SwiperSlide>
                ))}

            <SwiperSlide className=" border-3 border-main rounded-20  w-full flex justify-center items-center p-[20px]">
              <Link
                to={"/projects/add"}
                className="max-h-[60dvh] w-full flex flex-col justify-center items-center"
              >
                <span className="text-main font-bold text-20 text-center">
                  Создайте проект
                </span>
                <span className="text-[20dvh] font-light text-main">+</span>
                <span className="text-main font-bold text-20 text-center">
                  или посмотрите в галерее
                </span>
                <Gallery
                  height={"100px"}
                  width={"80px"}
                  widths={"1px"}
                  stroke="white"
                />
              </Link>
            </SwiperSlide>
          </Swiper>
        )}
      </div>
    </div>
  );
};

export { Home };
