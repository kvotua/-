import React from "react";
import { Outlet } from "react-router-dom";
import style from "./menu.module.css";

interface IMenu {
  handleClick?: () => void;
  Image: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
}

interface IMenuItem {
  menuItem: IMenu[];
}

const UiMenu: React.FC<IMenuItem> = ({ menuItem }) => {
  return (
    <>
      <Outlet />
      <div className="container">
        <nav className={style.menu}>
          <ul className="flex justify-between gap-[8vw]">
            {menuItem.map(({ handleClick, Image }, i) => (
              <li onClick={handleClick} key={i}>
                <Image stroke={"white"} />
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </>
  );
};

export { UiMenu };
