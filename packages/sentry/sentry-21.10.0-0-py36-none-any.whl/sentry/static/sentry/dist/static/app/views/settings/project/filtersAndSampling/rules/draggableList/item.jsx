Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
function Item({ value, dragging, index, transform, listeners, sorting, transition, forwardRef, attributes, renderItem, wrapperStyle, innerWrapperStyle, }) {
    return (<Wrapper ref={forwardRef} style={Object.assign(Object.assign({}, wrapperStyle), { transition, '--translate-x': transform ? `${Math.round(transform.x)}px` : undefined, '--translate-y': transform ? `${Math.round(transform.y)}px` : undefined, '--scale-x': (transform === null || transform === void 0 ? void 0 : transform.scaleX) ? `${transform.scaleX}` : undefined, '--scale-y': (transform === null || transform === void 0 ? void 0 : transform.scaleY) ? `${transform.scaleY}` : undefined })}>
      <InnerWrapper style={innerWrapperStyle}>
        {renderItem({
            dragging: Boolean(dragging),
            sorting: Boolean(sorting),
            listeners,
            transform,
            transition,
            value,
            index,
            attributes,
        })}
      </InnerWrapper>
    </Wrapper>);
}
exports.default = Item;
const boxShadowBorder = '0 0 0 calc(1px / var(--scale-x, 1)) rgba(63, 63, 68, 0.05)';
const boxShadowCommon = '0 1px calc(3px / var(--scale-x, 1)) 0 rgba(34, 33, 81, 0.15)';
const boxShadow = `${boxShadowBorder}, ${boxShadowCommon}`;
const Wrapper = (0, styled_1.default)('div') `
  transform: translate3d(var(--translate-x, 0), var(--translate-y, 0), 0)
    scaleX(var(--scale-x, 1)) scaleY(var(--scale-y, 1));
  transform-origin: 0 0;
  touch-action: manipulation;
  --box-shadow: ${boxShadow};
  --box-shadow-picked-up: ${boxShadowBorder}, -1px 0 15px 0 rgba(34, 33, 81, 0.01),
    0px 15px 15px 0 rgba(34, 33, 81, 0.25);
`;
const InnerWrapper = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.background};

  animation: pop 200ms cubic-bezier(0.18, 0.67, 0.6, 1.22);
  box-shadow: var(--box-shadow-picked-up);
  opacity: 1;

  :focus {
    box-shadow: 0 0px 4px 1px rgba(76, 159, 254, 1), ${boxShadow};
  }

  @keyframes pop {
    0% {
      transform: scale(1);
      box-shadow: var(--box-shadow);
    }
    100% {
      box-shadow: var(--box-shadow-picked-up);
    }
  }
`;
//# sourceMappingURL=item.jsx.map