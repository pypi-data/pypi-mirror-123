Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getSdkUpdateSuggestion_1 = (0, tslib_1.__importDefault)(require("app/utils/getSdkUpdateSuggestion"));
const SdkUpdates = ({ event }) => {
    const { sdkUpdates } = event;
    const eventDataSectinContent = sdkUpdates
        .map((sdkUpdate, index) => {
        const suggestion = (0, getSdkUpdateSuggestion_1.default)({ suggestion: sdkUpdate, sdk: event.sdk });
        if (!suggestion) {
            return null;
        }
        return (<alert_1.default key={index} type="info" icon={<icons_1.IconUpgrade />}>
          {(0, locale_1.tct)('We recommend you [suggestion] ', { suggestion })}
          {sdkUpdate.type === 'updateSdk' &&
                (0, locale_1.t)('(All sentry packages should be updated and their versions should match)')}
        </alert_1.default>);
    })
        .filter(alert => !!alert);
    if (!eventDataSectinContent.length) {
        return null;
    }
    return (<eventDataSection_1.default title={null} type="sdk-updates">
      {eventDataSectinContent}
    </eventDataSection_1.default>);
};
exports.default = SdkUpdates;
//# sourceMappingURL=index.jsx.map