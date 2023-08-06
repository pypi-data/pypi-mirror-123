Object.defineProperty(exports, "__esModule", { value: true });
exports.getShortEventId = exports.getTitle = exports.getTreeLabelPartDetails = exports.getLocation = exports.getMessage = void 0;
const types_1 = require("app/types");
const platform_1 = require("app/utils/platform");
function isTombstone(maybe) {
    return !maybe.hasOwnProperty('type');
}
/**
 * Extract the display message from an event.
 */
function getMessage(event) {
    if (isTombstone(event)) {
        return event.culprit || '';
    }
    const { metadata, type, culprit } = event;
    switch (type) {
        case types_1.EventOrGroupType.ERROR:
            return metadata.value;
        case types_1.EventOrGroupType.CSP:
            return metadata.message;
        case types_1.EventOrGroupType.EXPECTCT:
        case types_1.EventOrGroupType.EXPECTSTAPLE:
        case types_1.EventOrGroupType.HPKP:
            return '';
        default:
            return culprit || '';
    }
}
exports.getMessage = getMessage;
/**
 * Get the location from an event.
 */
function getLocation(event) {
    if (isTombstone(event)) {
        return undefined;
    }
    if (event.type === types_1.EventOrGroupType.ERROR && (0, platform_1.isNativePlatform)(event.platform)) {
        return event.metadata.filename || undefined;
    }
    return undefined;
}
exports.getLocation = getLocation;
function getTreeLabelPartDetails(part) {
    // Note: This function also exists in Python in eventtypes/base.py, to make
    // porting efforts simpler it's recommended to keep both variants
    // structurally similar.
    if (typeof part === 'string') {
        return part;
    }
    const label = (part === null || part === void 0 ? void 0 : part.function) || (part === null || part === void 0 ? void 0 : part.package) || (part === null || part === void 0 ? void 0 : part.filebase) || (part === null || part === void 0 ? void 0 : part.type);
    const classbase = part === null || part === void 0 ? void 0 : part.classbase;
    if (classbase) {
        return label ? `${classbase}.${label}` : classbase;
    }
    return label || '<unknown>';
}
exports.getTreeLabelPartDetails = getTreeLabelPartDetails;
function computeTitleWithTreeLabel(metadata) {
    const { type, current_tree_label, finest_tree_label } = metadata;
    const treeLabel = current_tree_label || finest_tree_label;
    const formattedTreeLabel = treeLabel
        ? treeLabel.map(labelPart => getTreeLabelPartDetails(labelPart)).join(' | ')
        : undefined;
    if (!type) {
        return {
            title: formattedTreeLabel || metadata.function || '<unknown>',
            treeLabel,
        };
    }
    if (!formattedTreeLabel) {
        return { title: type, treeLabel: undefined };
    }
    return {
        title: `${type} | ${formattedTreeLabel}`,
        treeLabel: [{ type }, ...(treeLabel !== null && treeLabel !== void 0 ? treeLabel : [])],
    };
}
function getTitle(event, features = [], grouping = false) {
    var _a, _b, _c, _d;
    const { metadata, type, culprit } = event;
    const customTitle = features.includes('custom-event-title') && (metadata === null || metadata === void 0 ? void 0 : metadata.title)
        ? metadata.title
        : undefined;
    switch (type) {
        case types_1.EventOrGroupType.ERROR: {
            if (customTitle) {
                return {
                    title: customTitle,
                    subtitle: culprit,
                    treeLabel: undefined,
                };
            }
            const displayTitleWithTreeLabel = features.includes('grouping-title-ui') &&
                (grouping ||
                    (0, platform_1.isNativePlatform)(event.platform) ||
                    (0, platform_1.isMobilePlatform)(event.platform));
            if (displayTitleWithTreeLabel) {
                return Object.assign({ subtitle: culprit }, computeTitleWithTreeLabel(metadata));
            }
            return {
                subtitle: culprit,
                title: metadata.type || metadata.function || '<unknown>',
                treeLabel: undefined,
            };
        }
        case types_1.EventOrGroupType.CSP:
            return {
                title: (_a = customTitle !== null && customTitle !== void 0 ? customTitle : metadata.directive) !== null && _a !== void 0 ? _a : '',
                subtitle: (_b = metadata.uri) !== null && _b !== void 0 ? _b : '',
                treeLabel: undefined,
            };
        case types_1.EventOrGroupType.EXPECTCT:
        case types_1.EventOrGroupType.EXPECTSTAPLE:
        case types_1.EventOrGroupType.HPKP:
            // Due to a regression some reports did not have message persisted
            // (https://github.com/getsentry/sentry/pull/19794) so we need to fall
            // back to the computed title for these.
            return {
                title: customTitle !== null && customTitle !== void 0 ? customTitle : (metadata.message || event.title),
                subtitle: (_c = metadata.origin) !== null && _c !== void 0 ? _c : '',
                treeLabel: undefined,
            };
        case types_1.EventOrGroupType.DEFAULT:
            return {
                title: (_d = customTitle !== null && customTitle !== void 0 ? customTitle : metadata.title) !== null && _d !== void 0 ? _d : '',
                subtitle: '',
                treeLabel: undefined,
            };
        default:
            return {
                title: customTitle !== null && customTitle !== void 0 ? customTitle : event.title,
                subtitle: '',
                treeLabel: undefined,
            };
    }
}
exports.getTitle = getTitle;
/**
 * Returns a short eventId with only 8 characters
 */
function getShortEventId(eventId) {
    return eventId.substring(0, 8);
}
exports.getShortEventId = getShortEventId;
//# sourceMappingURL=events.jsx.map