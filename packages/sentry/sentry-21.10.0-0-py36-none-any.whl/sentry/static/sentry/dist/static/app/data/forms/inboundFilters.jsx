Object.defineProperty(exports, "__esModule", { value: true });
exports.customFilterFields = exports.route = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/filters/';
const newLineHelpText = (0, locale_1.t)('Separate multiple entries with a newline.');
const globHelpText = (0, locale_1.tct)('Allows [link:glob pattern matching].', {
    link: <externalLink_1.default href="https://en.wikipedia.org/wiki/Glob_(programming)"/>,
});
const getOptionsData = (data) => ({ options: data });
const formGroups = [
    {
        // Form "section"/"panel"
        title: (0, locale_1.t)('Custom Filters'),
        fields: [
            {
                name: 'filters:blacklisted_ips',
                type: 'string',
                multiline: true,
                autosize: true,
                rows: 1,
                maxRows: 10,
                placeholder: 'e.g. 127.0.0.1 or 10.0.0.0/8',
                label: (0, locale_1.t)('IP Addresses'),
                help: (<react_1.Fragment>
            {(0, locale_1.t)('Filter events from these IP addresses. ')}
            {newLineHelpText}
          </react_1.Fragment>),
                getData: getOptionsData,
            },
        ],
    },
];
exports.default = formGroups;
// These require a feature flag
exports.customFilterFields = [
    {
        name: 'filters:releases',
        type: 'string',
        multiline: true,
        autosize: true,
        maxRows: 10,
        rows: 1,
        placeholder: 'e.g. 1.* or [!3].[0-9].*',
        label: (0, locale_1.t)('Releases'),
        help: (<react_1.Fragment>
        {(0, locale_1.t)('Filter events from these releases. ')}
        {newLineHelpText} {globHelpText}
      </react_1.Fragment>),
        getData: getOptionsData,
    },
    {
        name: 'filters:error_messages',
        type: 'string',
        multiline: true,
        autosize: true,
        maxRows: 10,
        rows: 1,
        placeholder: 'e.g. TypeError* or *: integer division or modulo by zero',
        label: (0, locale_1.t)('Error Message'),
        help: (<react_1.Fragment>
        {(0, locale_1.t)('Filter events by error messages. ')}
        {newLineHelpText} {globHelpText}
      </react_1.Fragment>),
        getData: getOptionsData,
    },
];
//# sourceMappingURL=inboundFilters.jsx.map