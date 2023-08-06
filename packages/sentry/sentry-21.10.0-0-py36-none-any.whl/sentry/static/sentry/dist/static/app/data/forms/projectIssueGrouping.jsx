Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const groupingInfo_1 = require("app/components/events/groupingInfo");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const marked_1 = (0, tslib_1.__importDefault)(require("app/utils/marked"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/issue-grouping/';
const groupingConfigField = {
    name: 'groupingConfig',
    type: 'select',
    label: (0, locale_1.t)('Grouping Config'),
    saveOnBlur: false,
    saveMessageAlertType: 'info',
    saveMessage: (0, locale_1.t)('Changing grouping config will apply to future events only (can take up to a minute).'),
    selectionInfoFunction: args => {
        const { groupingConfigs, value } = args;
        const selection = groupingConfigs.find(({ id }) => id === value);
        const changelog = (selection === null || selection === void 0 ? void 0 : selection.changelog) || '';
        if (!changelog) {
            return null;
        }
        return (<Changelog>
        <ChangelogTitle>
          {(0, locale_1.tct)('New in version [version]', { version: selection.id })}:
        </ChangelogTitle>
        <div dangerouslySetInnerHTML={{ __html: (0, marked_1.default)(changelog) }}/>
      </Changelog>);
    },
    choices: ({ groupingConfigs }) => groupingConfigs.map(({ id, hidden }) => [
        id.toString(),
        <groupingInfo_1.GroupingConfigItem key={id} isHidden={hidden}>
        {id}
      </groupingInfo_1.GroupingConfigItem>,
    ]),
    help: (0, locale_1.t)('Sets the grouping algorithm to be used for new events.'),
    visible: ({ features }) => features.has('set-grouping-config'),
};
exports.fields = {
    fingerprintingRules: {
        name: 'fingerprintingRules',
        type: 'string',
        label: (0, locale_1.t)('Fingerprint Rules'),
        hideLabel: true,
        placeholder: (0, locale_1.t)('error.type:MyException -> fingerprint-value\nstack.function:some_panic_function -> fingerprint-value'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: (0, locale_1.t)('Changing fingerprint rules will apply to future events only (can take up to a minute).'),
        formatMessageValue: false,
        help: () => (<react_1.Fragment>
        <RuleDescription>
          {(0, locale_1.tct)(`This can be used to modify the fingerprint rules on the server with custom rules.
        Rules follow the pattern [pattern]. To learn more about fingerprint rules, [docs:read the docs].`, {
                pattern: <code>matcher:glob -&gt; fingerprint, values</code>,
                docs: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/fingerprint-rules/"/>),
            })}
        </RuleDescription>
        <RuleExample>
          {`# force all errors of the same type to have the same fingerprint
error.type:DatabaseUnavailable -> system-down
# force all memory allocation errors to be grouped together
stack.function:malloc -> memory-allocation-error`}
        </RuleExample>
      </react_1.Fragment>),
        visible: true,
    },
    groupingEnhancements: {
        name: 'groupingEnhancements',
        type: 'string',
        label: (0, locale_1.t)('Stack Trace Rules'),
        hideLabel: true,
        placeholder: (0, locale_1.t)('stack.function:raise_an_exception ^-group\nstack.function:namespace::* +app'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: (0, locale_1.t)('Changing stack trace rules will apply to future events only (can take up to a minute).'),
        formatMessageValue: false,
        help: () => (<react_1.Fragment>
        <RuleDescription>
          {(0, locale_1.tct)(`This can be used to enhance the grouping algorithm with custom rules.
        Rules follow the pattern [pattern]. To learn more about stack trace rules, [docs:read the docs].`, {
                pattern: <code>matcher:glob [v^]?[+-]flag</code>,
                docs: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/stack-trace-rules/"/>),
            })}
        </RuleDescription>
        <RuleExample>
          {`# remove all frames above a certain function from grouping
stack.function:panic_handler ^-group
# mark all functions following a prefix in-app
stack.function:mylibrary_* +app`}
        </RuleExample>
      </react_1.Fragment>),
        validate: () => [],
        visible: true,
    },
    groupingConfig: groupingConfigField,
    secondaryGroupingConfig: Object.assign(Object.assign({}, groupingConfigField), { name: 'secondaryGroupingConfig', label: (0, locale_1.t)('Fallback/Secondary Grouping Config'), help: (0, locale_1.t)('Sets the secondary grouping algorithm that should be run in addition to avoid creating too many new groups. Controlled by expiration date below.'), saveMessage: (0, locale_1.t)('Changing the secondary grouping strategy will affect how many new issues are created.') }),
    secondaryGroupingExpiry: {
        name: 'secondaryGroupingExpiry',
        type: 'number',
        label: (0, locale_1.t)('Expiration date of secondary grouping'),
        help: (0, locale_1.t)('If this UNIX timestamp is in the past, the secondary grouping configuration stops applying automatically.'),
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: (0, locale_1.t)('Changing the expiration date will affect how many new issues are created.'),
    },
};
const RuleDescription = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
  margin-top: -${(0, space_1.default)(1)};
  margin-right: 36px;
`;
const RuleExample = (0, styled_1.default)('pre') `
  margin-bottom: ${(0, space_1.default)(1)};
  margin-right: 36px;
`;
const Changelog = (0, styled_1.default)('div') `
  position: relative;
  top: -1px;
  margin-bottom: -1px;
  padding: ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  background: ${p => p.theme.backgroundSecondary};
  font-size: ${p => p.theme.fontSizeMedium};

  &:last-child {
    border: 0;
    border-bottom-left-radius: ${p => p.theme.borderRadius};
    border-bottom-right-radius: ${p => p.theme.borderRadius};
  }
`;
const ChangelogTitle = (0, styled_1.default)('h3') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(0.75)} !important;
`;
//# sourceMappingURL=projectIssueGrouping.jsx.map