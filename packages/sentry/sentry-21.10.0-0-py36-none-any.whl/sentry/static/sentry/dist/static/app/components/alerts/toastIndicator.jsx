Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const framer_motion_1 = require("framer-motion");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
function ToastIndicator(_a) {
    var { indicator, onDismiss, className } = _a, props = (0, tslib_1.__rest)(_a, ["indicator", "onDismiss", "className"]);
    let icon;
    const { options, message, type } = indicator;
    const { undo, disableDismiss } = options || {};
    const showUndo = typeof undo === 'function';
    const handleClick = (e) => {
        if (disableDismiss) {
            return;
        }
        if (typeof onDismiss === 'function') {
            onDismiss(indicator, e);
        }
    };
    if (type === 'success') {
        icon = <icons_1.IconCheckmark size="lg" isCircled/>;
    }
    else if (type === 'error') {
        icon = <icons_1.IconClose size="lg" isCircled/>;
    }
    // TODO(billy): Remove ref- className after removing usage from getsentry
    return (<Toast onClick={handleClick} data-test-id={type ? `toast-${type}` : 'toast'} className={(0, classnames_1.default)(className, 'ref-toast', `ref-${type}`)} {...props}>
      {type === 'loading' ? (<StyledLoadingIndicator mini/>) : (<Icon type={type}>{icon}</Icon>)}
      <Message>{message}</Message>
      {showUndo && <Undo onClick={undo}>{(0, locale_1.t)('Undo')}</Undo>}
    </Toast>);
}
const Toast = (0, styled_1.default)(framer_motion_1.motion.div) `
  display: flex;
  align-items: center;
  height: 40px;
  padding: 0 15px 0 10px;
  margin-top: 15px;
  background: ${p => p.theme.gray500};
  color: #fff;
  border-radius: 44px 7px 7px 44px;
  box-shadow: 0 4px 12px 0 rgba(47, 40, 55, 0.16);
  position: relative;
`;
Toast.defaultProps = {
    initial: {
        opacity: 0,
        y: 70,
    },
    animate: {
        opacity: 1,
        y: 0,
    },
    exit: {
        opacity: 0,
        y: 70,
    },
    transition: (0, testableTransition_1.default)({
        type: 'spring',
        stiffness: 450,
        damping: 25,
    }),
};
const Icon = (0, styled_1.default)('div', { shouldForwardProp: p => p !== 'type' }) `
  margin-right: ${(0, space_1.default)(0.75)};
  svg {
    display: block;
  }

  color: ${p => (p.type === 'success' ? p.theme.green300 : p.theme.red300)};
`;
const Message = (0, styled_1.default)('div') `
  flex: 1;
`;
const Undo = (0, styled_1.default)('div') `
  display: inline-block;
  color: ${p => p.theme.gray300};
  padding-left: ${(0, space_1.default)(2)};
  margin-left: ${(0, space_1.default)(2)};
  border-left: 1px solid ${p => p.theme.gray200};
  cursor: pointer;

  &:hover {
    color: ${p => p.theme.gray200};
  }
`;
const StyledLoadingIndicator = (0, styled_1.default)(loadingIndicator_1.default) `
  .loading-indicator {
    border-color: ${p => p.theme.gray500};
    border-left-color: ${p => p.theme.purple300};
  }
`;
exports.default = ToastIndicator;
//# sourceMappingURL=toastIndicator.jsx.map