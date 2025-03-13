import React from 'react';
import classNames from 'classnames';

const Card = ({ 
  title, 
  children, 
  className,
  headerClassName,
  bodyClassName 
}) => {
  return (
    <div className={classNames('card', className)}>
      {title && (
        <div className={classNames('mb-4', headerClassName)}>
          <h2 className="text-xl font-semibold">{title}</h2>
        </div>
      )}
      <div className={classNames(bodyClassName)}>
        {children}
      </div>
    </div>
  );
};

export default Card;