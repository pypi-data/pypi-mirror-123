Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const scoreBar_1 = (0, tslib_1.__importDefault)(require("app/components/scoreBar"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const chartPalette_1 = (0, tslib_1.__importDefault)(require("app/constants/chartPalette"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
function UserMisery(props) {
    const { bars, barHeight, userMisery, miseryLimit, totalUsers, miserableUsers } = props;
    // User Misery will always be > 0 because of the maximum a posteriori estimate
    // and below 5% will always be an overestimation of the actual proportion
    // of miserable to total unique users. We are going to visualize it as
    // 0 User Misery while still preserving the actual value for sorting purposes.
    const adjustedMisery = userMisery > 0.05 ? userMisery : 0;
    const palette = new Array(bars).fill([chartPalette_1.default[0][0]]);
    const score = Math.round(adjustedMisery * palette.length);
    let title;
    if ((0, utils_1.defined)(miserableUsers) && (0, utils_1.defined)(totalUsers) && (0, utils_1.defined)(miseryLimit)) {
        title = (0, locale_1.tct)('[miserableUsers] out of [totalUsers] unique users waited more than [duration]ms (4x the response time threshold)', {
            miserableUsers,
            totalUsers,
            duration: 4 * miseryLimit,
        });
    }
    else if ((0, utils_1.defined)(miseryLimit)) {
        title = (0, locale_1.tct)('User Misery score is [userMisery], representing users who waited more than more than [duration]ms (4x the response time threshold)', {
            duration: 4 * miseryLimit,
            userMisery: userMisery.toFixed(3),
        });
    }
    else {
        title = (0, locale_1.tct)('User Misery score is [userMisery].', {
            userMisery: userMisery.toFixed(3),
        });
    }
    return (<tooltip_1.default title={title} containerDisplayMode="block">
      <scoreBar_1.default size={barHeight} score={score} palette={palette} radius={0}/>
    </tooltip_1.default>);
}
exports.default = UserMisery;
//# sourceMappingURL=userMisery.jsx.map