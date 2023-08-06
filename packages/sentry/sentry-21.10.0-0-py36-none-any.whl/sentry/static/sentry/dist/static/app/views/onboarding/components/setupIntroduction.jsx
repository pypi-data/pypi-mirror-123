Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const platformicons_1 = require("platformicons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const stepHeading_1 = (0, tslib_1.__importDefault)(require("./stepHeading"));
function SetupIntroduction({ stepHeaderText, platform }) {
    return (<TitleContainer>
      <stepHeading_1.default step={2}>{stepHeaderText}</stepHeading_1.default>
      <framer_motion_1.motion.div variants={{
            initial: { opacity: 0, x: 20 },
            animate: { opacity: 1, x: 0 },
            exit: { opacity: 0 },
        }}>
        <platformicons_1.PlatformIcon size={48} format="lg" platform={platform}/>
      </framer_motion_1.motion.div>
    </TitleContainer>);
}
exports.default = SetupIntroduction;
const TitleContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(2)};
  align-items: center;
  justify-items: end;

  ${stepHeading_1.default} {
    margin-bottom: 0;
  }
`;
//# sourceMappingURL=setupIntroduction.jsx.map