Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const timeSince_1 = (0, tslib_1.__importStar)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const GroupInboxReason = {
    NEW: 0,
    UNIGNORED: 1,
    REGRESSION: 2,
    MANUAL: 3,
    REPROCESSED: 4,
};
const EVENT_ROUND_LIMIT = 1000;
function InboxReason({ inbox, fontSize = 'sm', showDateAdded }) {
    const { reason, reason_details: reasonDetails, date_added: dateAdded } = inbox;
    const relativeDateAdded = (0, getDynamicText_1.default)({
        value: dateAdded && (0, timeSince_1.getRelativeDate)(dateAdded, 'ago', true),
        fixed: '3s ago',
    });
    const getCountText = (count) => count > EVENT_ROUND_LIMIT
        ? `More than ${Math.round(count / EVENT_ROUND_LIMIT)}k`
        : `${count}`;
    function getTooltipDescription() {
        const { until, count, window, user_count: userCount, user_window: userWindow, } = reasonDetails;
        if (until) {
            // Was ignored until `until` has passed.
            // `until` format: "2021-01-20T03:59:03+00:00"
            return (0, locale_1.tct)('Was ignored until [window]', {
                window: <dateTime_1.default date={until} dateOnly/>,
            });
        }
        if (count) {
            // Was ignored until `count` events occurred
            // If `window` is defined, than `count` events occurred in `window` minutes.
            // else `count` events occurred since it was ignored.
            if (window) {
                return (0, locale_1.tct)('Occurred [count] time(s) in [duration]', {
                    count: getCountText(count),
                    duration: (0, formatters_1.getDuration)(window * 60, 0, true),
                });
            }
            return (0, locale_1.tct)('Occurred [count] time(s)', {
                count: getCountText(count),
            });
        }
        if (userCount) {
            // Was ignored until `user_count` users were affected
            // If `user_window` is defined, than `user_count` users affected in `user_window` minutes.
            // else `user_count` events occurred since it was ignored.
            if (userWindow) {
                return (0, locale_1.tct)('Affected [count] user(s) in [duration]', {
                    count: getCountText(userCount),
                    duration: (0, formatters_1.getDuration)(userWindow * 60, 0, true),
                });
            }
            return (0, locale_1.tct)('Affected [count] user(s)', {
                count: getCountText(userCount),
            });
        }
        return undefined;
    }
    function getReasonDetails() {
        switch (reason) {
            case GroupInboxReason.UNIGNORED:
                return {
                    tagType: 'default',
                    reasonBadgeText: (0, locale_1.t)('Unignored'),
                    tooltipText: dateAdded &&
                        (0, locale_1.t)('Unignored %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                    tooltipDescription: getTooltipDescription(),
                };
            case GroupInboxReason.REGRESSION:
                return {
                    tagType: 'error',
                    reasonBadgeText: (0, locale_1.t)('Regression'),
                    tooltipText: dateAdded &&
                        (0, locale_1.t)('Regressed %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                    // TODO: Add tooltip description for regression move when resolver is added to reason
                    // Resolved by {full_name} {time} ago.
                };
            // TODO: Manual moves will go away, remove this then
            case GroupInboxReason.MANUAL:
                return {
                    tagType: 'highlight',
                    reasonBadgeText: (0, locale_1.t)('Manual'),
                    tooltipText: dateAdded && (0, locale_1.t)('Moved %(relative)s', { relative: relativeDateAdded }),
                    // TODO: IF manual moves stay then add tooltip description for manual move
                    // Moved to inbox by {full_name}.
                };
            case GroupInboxReason.REPROCESSED:
                return {
                    tagType: 'info',
                    reasonBadgeText: (0, locale_1.t)('Reprocessed'),
                    tooltipText: dateAdded &&
                        (0, locale_1.t)('Reprocessed %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                };
            case GroupInboxReason.NEW:
            default:
                return {
                    tagType: 'warning',
                    reasonBadgeText: (0, locale_1.t)('New Issue'),
                    tooltipText: dateAdded &&
                        (0, locale_1.t)('Created %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                };
        }
    }
    const { tooltipText, tooltipDescription, reasonBadgeText, tagType } = getReasonDetails();
    const tooltip = (tooltipText || tooltipDescription) && (<TooltipWrapper>
      {tooltipText && <div>{tooltipText}</div>}
      {tooltipDescription && (<TooltipDescription>{tooltipDescription}</TooltipDescription>)}
      <TooltipDescription>Mark Reviewed to remove this label</TooltipDescription>
    </TooltipWrapper>);
    return (<StyledTag type={tagType} tooltipText={tooltip} fontSize={fontSize}>
      {reasonBadgeText}
      {showDateAdded && dateAdded && (<React.Fragment>
          <Separator type={tagType !== null && tagType !== void 0 ? tagType : 'default'}>{' | '}</Separator>
          <timeSince_1.default date={dateAdded} suffix="" extraShort disabledAbsoluteTooltip/>
        </React.Fragment>)}
    </StyledTag>);
}
exports.default = InboxReason;
const TooltipWrapper = (0, styled_1.default)('div') `
  text-align: left;
`;
const TooltipDescription = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
`;
const Separator = (0, styled_1.default)('span') `
  color: ${p => p.theme.tag[p.type].iconColor};
  opacity: 80%;
`;
const StyledTag = (0, styled_1.default)(tag_1.default, {
    shouldForwardProp: p => p !== 'fontSize',
}) `
  font-size: ${p => p.fontSize === 'sm' ? p.theme.fontSizeSmall : p.theme.fontSizeMedium};
`;
//# sourceMappingURL=inboxReason.jsx.map