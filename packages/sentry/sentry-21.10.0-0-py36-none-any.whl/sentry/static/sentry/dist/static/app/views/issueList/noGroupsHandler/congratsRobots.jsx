Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const congrats_robots_mp4_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/congrats-robots.mp4"));
const autoplayVideo_1 = (0, tslib_1.__importDefault)(require("app/components/autoplayVideo"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
/**
 * Note, video needs `muted` for `autoplay` to work on Chrome
 * See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
 */
function CongratsRobots() {
    return (<AnimatedScene>
      <StyledAutoplayVideo src={congrats_robots_mp4_1.default}/>
    </AnimatedScene>);
}
exports.default = CongratsRobots;
const AnimatedScene = (0, styled_1.default)('div') `
  max-width: 800px;
`;
const StyledAutoplayVideo = (0, styled_1.default)(autoplayVideo_1.default) `
  max-height: 320px;
  max-width: 100%;
  margin-bottom: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=congratsRobots.jsx.map