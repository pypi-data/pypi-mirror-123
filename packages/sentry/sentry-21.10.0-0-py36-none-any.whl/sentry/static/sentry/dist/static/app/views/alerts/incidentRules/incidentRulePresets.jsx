Object.defineProperty(exports, "__esModule", { value: true });
exports.makeDefaultCta = void 0;
const locale_1 = require("app/locale");
const types_1 = require("app/utils/discover/types");
const getIncidentRuleDiscoverUrl_1 = require("app/views/alerts/utils/getIncidentRuleDiscoverUrl");
/**
 * Get the CTA used for alert rules that do not have a preset
 */
function makeDefaultCta({ orgSlug, projects, rule, eventType, start, end, }) {
    if (!rule) {
        return {
            buttonText: (0, locale_1.t)('Open in Discover'),
            to: '',
        };
    }
    const extraQueryParams = {
        display: types_1.DisplayModes.TOP5,
    };
    return {
        buttonText: (0, locale_1.t)('Open in Discover'),
        to: (0, getIncidentRuleDiscoverUrl_1.getIncidentRuleDiscoverUrl)({
            orgSlug,
            projects,
            rule,
            eventType,
            start,
            end,
            extraQueryParams,
        }),
    };
}
exports.makeDefaultCta = makeDefaultCta;
//# sourceMappingURL=incidentRulePresets.jsx.map