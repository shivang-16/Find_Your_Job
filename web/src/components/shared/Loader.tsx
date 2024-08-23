import React from 'react';
import { ClipLoader } from 'react-spinners';

interface LoaderProps {
  size?: number;
  color?: string;
  loaderClassName?: string;
}

const Loader: React.FC<LoaderProps> = ({
  size = 15,
  color = "rgba(59, 130, 246, 1)",
  loaderClassName = "loading",
}) => {
  return (
    <div className={loaderClassName}>
      <ClipLoader size={size} color={color} />
    </div>
  );
};

export default Loader;