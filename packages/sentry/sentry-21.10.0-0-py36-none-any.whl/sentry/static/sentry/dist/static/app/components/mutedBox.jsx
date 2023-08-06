Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const styles_1 = require("app/components/events/styles");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
function MutedBox({ statusDetails }) {
    function renderReason() {
        const { ignoreUntil, ignoreCount, ignoreWindow, ignoreUserCount, ignoreUserWindow } = statusDetails;
        if (ignoreUntil) {
            return (0, locale_1.t)('This issue has been ignored until %s', <strong>
          <dateTime_1.default date={ignoreUntil}/>
        </strong>);
        }
        else if (ignoreCount && ignoreWindow) {
            return (0, locale_1.t)('This issue has been ignored until it occurs %s time(s) in %s', <strong>{ignoreCount.toLocaleString()}</strong>, <strong>
          <duration_1.default seconds={ignoreWindow * 60}/>
        </strong>);
        }
        else if (ignoreCount) {
            return (0, locale_1.t)('This issue has been ignored until it occurs %s more time(s)', <strong>{ignoreCount.toLocaleString()}</strong>);
        }
        else if (ignoreUserCount && ignoreUserWindow) {
            return (0, locale_1.t)('This issue has been ignored until it affects %s user(s) in %s', <strong>{ignoreUserCount.toLocaleString()}</strong>, <strong>
          <duration_1.default seconds={ignoreUserWindow * 60}/>
        </strong>);
        }
        else if (ignoreUserCount) {
            return (0, locale_1.t)('This issue has been ignored until it affects %s more user(s)', <strong>{ignoreUserCount.toLocaleString()}</strong>);
        }
        return (0, locale_1.t)('This issue has been ignored');
    }
    return (<styles_1.BannerContainer priority="default">
      <styles_1.BannerSummary>
        <icons_1.IconMute color="red300" size="sm"/>
        <span>
          {renderReason()}&nbsp;&mdash;&nbsp;
          {(0, locale_1.t)('You will not be notified of any changes and it will not show up by default in feeds.')}
        </span>
      </styles_1.BannerSummary>
    </styles_1.BannerContainer>);
}
exports.default = MutedBox;
//# sourceMappingURL=mutedBox.jsx.map