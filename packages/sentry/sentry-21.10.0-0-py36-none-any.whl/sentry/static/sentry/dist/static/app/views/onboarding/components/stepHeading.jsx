Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const StepHeading = (0, styled_1.default)(framer_motion_1.motion.h2) `
  margin-left: calc(-${(0, space_1.default)(2)} - 30px);
  position: relative;
  display: inline-grid;
  grid-template-columns: max-content max-content;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;

  &:before {
    content: '${p => p.step}';
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    background-color: ${p => p.theme.yellow300};
    border-radius: 50%;
    color: ${p => p.theme.textColor};
    font-size: 1.5rem;
  }
`;
StepHeading.defaultProps = {
    variants: {
        initial: { clipPath: 'inset(0% 100% 0% 0%)', opacity: 1 },
        animate: { clipPath: 'inset(0% 0% 0% 0%)', opacity: 1 },
        exit: { opacity: 0 },
    },
    transition: (0, testableTransition_1.default)({
        duration: 0.3,
    }),
};
exports.default = StepHeading;
//# sourceMappingURL=stepHeading.jsx.map