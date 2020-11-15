import PropTypes from 'prop-types';
import React from 'react';
import styled, { keyframes } from 'styled-components';
import { appColor } from '../modules/theme';

const px = value => (typeof value === 'number' ? `${value}px` : value);

const grow = props => keyframes`
  0% {
    height: 0;
    width: 0;
  }

  30% {
    border-width: ${px(props.size && props.size / 2.5)};
    opacity: 1;
  }

  100% {
    border-width: 0;
    height: ${px(props.size)};
    opacity: 0;
    width: ${px(props.size)};
  }
`;

const rotate = keyframes`
  100% {
    transform: rotate(360deg);
  }
`;

const ripple = props => keyframes`
  0% {
    height: 0;
    left: ${px(props.size / 2)};
    opacity: 1;
    top: ${px(props.size / 2)};
    width: 0;
  }

  100% {
    height: ${px(props.size)};
    left: 0;
    opacity: 0;
    top: 0;
    width: ${px(props.size)};
  }
`;

/* stylelint-disable unit-blacklist */
const dash = keyframes`
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35px;
  }

  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124px;
  }
`;
/* stylelint-enable unit-blacklist */

const LoaderGrow = styled.div`
  display: ${props => (props.block ? 'flex' : 'inline-flex')};
  height: ${props => px(props.size)};
  margin: ${props => (props.block ? '2rem' : 0)} auto;
  position: relative;
  width: ${props => px(props.size)};

  > div {
    animation: ${grow} 1.15s infinite cubic-bezier(0.2, 0.6, 0.36, 1);
    border: 0 solid ${props => props.color};
    border-radius: 50%;
    box-sizing: border-box;
    height: 0;
    left: 50%;
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 0;
  }
`;

const LoaderPulse = styled.div`
  display: ${props => (props.block ? 'flex' : 'inline-flex')};
  height: ${props => px(props.size)};
  margin: ${props => (props.block ? '2rem' : 0)} auto;
  position: relative;
  width: ${props => px(props.size)};

  > div {
    animation: ${ripple} 1.2s cubic-bezier(0, 0.2, 0.8, 1) infinite;
    border: ${props => px(Math.round(props.size / 16))} solid ${props => props.color};
    border-radius: 50%;
    opacity: 1;
    position: absolute;
  }

  > div:nth-child(2) {
    animation-delay: -0.5s;
  }
`;

const LoaderRotate = styled.div`
  display: ${props => (props.block ? 'flex' : 'inline-flex')};
  margin: ${props => (props.block ? '2rem' : 0)} auto;
  text-align: center;
`;

const LoaderRotateSVG = styled.svg.attrs({
  viewBox: '25 25 50 50',
})`
  animation: ${rotate} 2s linear infinite;
  height: ${props => px(props.size)};
  margin: auto;
  transform-origin: center center;
  width: ${props => px(props.size)};
`;

const LoaderRotateCircle = styled.circle`
  animation: ${dash} 1.5s ease-in-out infinite;
  stroke: ${props => props.color};
  stroke-dasharray: 1, 200;
  stroke-dashoffset: 0;
  stroke-linecap: round;
`;

const Loader = props => {
  let html;

  if (props.type === 'rotate') {
    html = (
      <LoaderRotate {...props}>
        <LoaderRotateSVG {...props}>
          <LoaderRotateCircle {...props} cx="50" cy="50" r="20" fill="none" strokeWidth={2} />
        </LoaderRotateSVG>
      </LoaderRotate>
    );
  } else if (props.type === 'pulse') {
    html = (
      <LoaderPulse {...props}>
        <div />
        <div />
      </LoaderPulse>
    );
  } else {
    html = (
      <LoaderGrow {...props}>
        <div />
      </LoaderGrow>
    );
  }

  return html;
};

Loader.propTypes = {
  block: PropTypes.bool,
  color: PropTypes.string,
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  type: PropTypes.oneOf(['grow', 'pulse', 'rotate']),
};

Loader.defaultProps = {
  block: false,
  color: appColor,
  size: 32,
  type: 'grow',
};

export default Loader;
