Object.defineProperty(exports, "__esModule", { value: true });
exports.getParentField = exports.getStateToPutForParent = exports.getStateToPutForDefault = exports.getStateToPutForProvider = exports.isSufficientlyComplex = exports.getParentData = exports.getParentValues = exports.getParentIds = exports.isEverythingDisabled = exports.decideDefault = exports.getCurrentDefault = exports.getCurrentProviders = exports.getUserDefaultValues = exports.mergeNotificationSettings = exports.backfillMissingProvidersWithFallback = exports.getChoiceString = exports.providerListToString = exports.getFallBackValue = exports.groupByOrganization = exports.getParentKey = exports.isGroupedByProject = void 0;
const tslib_1 = require("tslib");
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const locale_1 = require("app/locale");
const constants_1 = require("app/views/settings/account/notifications/constants");
const fields2_1 = require("app/views/settings/account/notifications/fields2");
const parentLabel_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/notifications/parentLabel"));
/**
 * Which fine-tuning parts are grouped by project
 */
const isGroupedByProject = (notificationType) => ['alerts', 'email', 'workflow'].includes(notificationType);
exports.isGroupedByProject = isGroupedByProject;
const getParentKey = (notificationType) => {
    return (0, exports.isGroupedByProject)(notificationType) ? 'project' : 'organization';
};
exports.getParentKey = getParentKey;
const groupByOrganization = (projects) => {
    return projects.reduce((acc, project) => {
        const orgSlug = project.organization.slug;
        if (acc.hasOwnProperty(orgSlug)) {
            acc[orgSlug].projects.push(project);
        }
        else {
            acc[orgSlug] = {
                organization: project.organization,
                projects: [project],
            };
        }
        return acc;
    }, {});
};
exports.groupByOrganization = groupByOrganization;
const getFallBackValue = (notificationType) => {
    switch (notificationType) {
        case 'alerts':
            return 'always';
        case 'deploy':
            return 'committed_only';
        case 'workflow':
            return 'subscribe_only';
        default:
            return '';
    }
};
exports.getFallBackValue = getFallBackValue;
const providerListToString = (providers) => {
    return providers.sort().join('+');
};
exports.providerListToString = providerListToString;
const getChoiceString = (choices, key) => {
    if (!choices) {
        return 'default';
    }
    const found = choices.find(row => row[0] === key);
    if (!found) {
        throw new Error(`Could not find ${key}`);
    }
    return found[1];
};
exports.getChoiceString = getChoiceString;
/**
 * Transform `data`, a mapping of providers to values, so that all providers in
 * `providerList` are "on" in the resulting object. The "on" value is
 * determined by checking `data` for non-"never" values and falling back to the
 * value `fallbackValue`. The "off" value is either "default" or "never"
 * depending on whether `scopeType` is "parent" or "user" respectively.
 */
const backfillMissingProvidersWithFallback = (data, providerList, fallbackValue, scopeType) => {
    // First pass: determine the fallback value.
    const fallback = Object.values(data).reduce((previousValue, currentValue) => currentValue === 'never' ? previousValue : currentValue, fallbackValue);
    // Second pass: fill in values for every provider.
    return Object.fromEntries(Object.keys(constants_1.ALL_PROVIDERS).map(provider => [
        provider,
        providerList.includes(provider)
            ? fallback
            : scopeType === 'user'
                ? 'never'
                : 'default',
    ]));
};
exports.backfillMissingProvidersWithFallback = backfillMissingProvidersWithFallback;
/**
 * Deeply merge N notification settings objects (usually just 2).
 */
const mergeNotificationSettings = (...objects) => {
    const output = {};
    objects.map(settingsByType => Object.entries(settingsByType).map(([type, settingsByScopeType]) => Object.entries(settingsByScopeType).map(([scopeType, settingsByScopeId]) => Object.entries(settingsByScopeId).map(([scopeId, settingsByProvider]) => {
        (0, set_1.default)(output, [type, scopeType, scopeId].join('.'), settingsByProvider);
    }))));
    return output;
};
exports.mergeNotificationSettings = mergeNotificationSettings;
/**
 * Get the mapping of providers to values that describe a user's parent-
 * independent notification preferences. The data from the API uses the user ID
 * rather than "me" so we assume the first ID is the user's.
 */
const getUserDefaultValues = (notificationType, notificationSettings) => {
    var _a;
    return (Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a.user) || {}).pop() ||
        Object.fromEntries(Object.entries(constants_1.ALL_PROVIDERS).map(([provider, value]) => [
            provider,
            value === 'default' ? (0, exports.getFallBackValue)(notificationType) : value,
        ])));
};
exports.getUserDefaultValues = getUserDefaultValues;
/**
 * Get the list of providers currently active on this page. Note: this can be empty.
 */
const getCurrentProviders = (notificationType, notificationSettings) => {
    const userData = (0, exports.getUserDefaultValues)(notificationType, notificationSettings);
    return Object.entries(userData)
        .filter(([_, value]) => !['never'].includes(value))
        .map(([provider, _]) => provider);
};
exports.getCurrentProviders = getCurrentProviders;
/**
 * Calculate the currently selected provider.
 */
const getCurrentDefault = (notificationType, notificationSettings) => {
    const providersList = (0, exports.getCurrentProviders)(notificationType, notificationSettings);
    return providersList.length
        ? (0, exports.getUserDefaultValues)(notificationType, notificationSettings)[providersList[0]]
        : 'never';
};
exports.getCurrentDefault = getCurrentDefault;
/**
 * For a given notificationType, are the parent-independent setting "never" for
 * all providers and are the parent-specific settings "default" or "never". If
 * so, the API is telling us that the user has opted out of all notifications.
 */
const decideDefault = (notificationType, notificationSettings) => {
    var _a;
    const compare = (a, b) => constants_1.VALUE_MAPPING[a] - constants_1.VALUE_MAPPING[b];
    const parentIndependentSetting = Object.values((0, exports.getUserDefaultValues)(notificationType, notificationSettings))
        .sort(compare)
        .pop() || 'never';
    if (parentIndependentSetting !== 'never') {
        return parentIndependentSetting;
    }
    const parentSpecificSetting = Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a[(0, exports.getParentKey)(notificationType)]) || {})
        .flatMap(settingsByProvider => Object.values(settingsByProvider))
        .sort(compare)
        .pop() || 'default';
    return parentSpecificSetting === 'default' ? 'never' : parentSpecificSetting;
};
exports.decideDefault = decideDefault;
/**
 * For a given notificationType, are the parent-independent setting "never" for
 * all providers and are the parent-specific settings "default" or "never"? If
 * so, the API is telling us that the user has opted out of all notifications.
 */
const isEverythingDisabled = (notificationType, notificationSettings) => ['never', 'default'].includes((0, exports.decideDefault)(notificationType, notificationSettings));
exports.isEverythingDisabled = isEverythingDisabled;
/**
 * Extract either the list of project or organization IDs from the notification
 * settings in state. This assumes that the notification settings object is
 * fully backfilled with settings for every parent.
 */
const getParentIds = (notificationType, notificationSettings) => {
    var _a;
    return Object.keys(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a[(0, exports.getParentKey)(notificationType)]) || {});
};
exports.getParentIds = getParentIds;
const getParentValues = (notificationType, notificationSettings, parentId) => {
    var _a, _b;
    return ((_b = (_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a[(0, exports.getParentKey)(notificationType)]) === null || _b === void 0 ? void 0 : _b[parentId]) || {
        email: 'default',
    };
};
exports.getParentValues = getParentValues;
/**
 * Get a mapping of all parent IDs to the notification setting for the current
 * providers.
 */
const getParentData = (notificationType, notificationSettings, parents) => {
    const provider = (0, exports.getCurrentProviders)(notificationType, notificationSettings)[0];
    return Object.fromEntries(parents.map(parent => [
        parent.id,
        (0, exports.getParentValues)(notificationType, notificationSettings, parent.id)[provider],
    ]));
};
exports.getParentData = getParentData;
/**
 * Are there are more than N project or organization settings?
 */
const isSufficientlyComplex = (notificationType, notificationSettings) => (0, exports.getParentIds)(notificationType, notificationSettings).length >
    constants_1.MIN_PROJECTS_FOR_CONFIRMATION;
exports.isSufficientlyComplex = isSufficientlyComplex;
/**
 * I don't need to update the provider for EVERY once of the user's projects
 * and organizations, just the user and parents that have explicit settings.
 */
const getStateToPutForProvider = (notificationType, notificationSettings, changedData) => {
    const providerList = changedData.provider.split('+');
    const fallbackValue = (0, exports.getFallBackValue)(notificationType);
    // If the user has no settings, we need to create them.
    if (!Object.keys(notificationSettings).length) {
        return {
            [notificationType]: {
                user: {
                    me: Object.fromEntries(providerList.map(provider => [provider, fallbackValue])),
                },
            },
        };
    }
    return {
        [notificationType]: Object.fromEntries(Object.entries(notificationSettings[notificationType]).map(([scopeType, scopeTypeData]) => [
            scopeType,
            Object.fromEntries(Object.entries(scopeTypeData).map(([scopeId, scopeIdData]) => [
                scopeId,
                (0, exports.backfillMissingProvidersWithFallback)(scopeIdData, providerList, fallbackValue, scopeType),
            ])),
        ])),
    };
};
exports.getStateToPutForProvider = getStateToPutForProvider;
/**
 * Update the current providers' parent-independent notification settings with
 * the new value. If the new value is "never", then also update all
 * parent-specific notification settings to "default". If the previous value
 * was "never", then assume providerList should be "email" only.
 */
const getStateToPutForDefault = (notificationType, notificationSettings, changedData, parentIds) => {
    const newValue = Object.values(changedData)[0];
    let providerList = (0, exports.getCurrentProviders)(notificationType, notificationSettings);
    if (!providerList.length) {
        providerList = ['email'];
    }
    const updatedNotificationSettings = {
        [notificationType]: {
            user: {
                me: Object.fromEntries(providerList.map(provider => [provider, newValue])),
            },
        },
    };
    if (newValue === 'never') {
        updatedNotificationSettings[notificationType][(0, exports.getParentKey)(notificationType)] =
            Object.fromEntries(parentIds.map(parentId => [
                parentId,
                Object.fromEntries(providerList.map(provider => [provider, 'default'])),
            ]));
    }
    return updatedNotificationSettings;
};
exports.getStateToPutForDefault = getStateToPutForDefault;
/**
 * Get the diff of the Notification Settings for this parent ID.
 */
const getStateToPutForParent = (notificationType, notificationSettings, changedData, parentId) => {
    const providerList = (0, exports.getCurrentProviders)(notificationType, notificationSettings);
    const newValue = Object.values(changedData)[0];
    return {
        [notificationType]: {
            [(0, exports.getParentKey)(notificationType)]: {
                [parentId]: Object.fromEntries(providerList.map(provider => [provider, newValue])),
            },
        },
    };
};
exports.getStateToPutForParent = getStateToPutForParent;
/**
 * Render each parent and add a default option to the the field choices.
 */
const getParentField = (notificationType, notificationSettings, parent, onChange) => {
    var _a;
    const defaultFields = fields2_1.NOTIFICATION_SETTING_FIELDS[notificationType];
    return Object.assign({}, defaultFields, {
        label: <parentLabel_1.default parent={parent} notificationType={notificationType}/>,
        getData: data => onChange(data, parent.id),
        name: parent.id,
        choices: (_a = defaultFields.choices) === null || _a === void 0 ? void 0 : _a.concat([
            [
                'default',
                `${(0, locale_1.t)('Default')} (${(0, exports.getChoiceString)(defaultFields.choices, (0, exports.getCurrentDefault)(notificationType, notificationSettings))})`,
            ],
        ]),
        defaultValue: 'default',
        help: undefined,
    });
};
exports.getParentField = getParentField;
//# sourceMappingURL=utils.jsx.map