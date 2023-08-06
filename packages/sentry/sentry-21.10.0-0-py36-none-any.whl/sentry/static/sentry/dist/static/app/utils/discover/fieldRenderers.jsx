Object.defineProperty(exports, "__esModule", { value: true });
exports.getFieldFormatter = exports.getFieldRenderer = exports.getSortField = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const partial_1 = (0, tslib_1.__importDefault)(require("lodash/partial"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const userBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/userBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const rowBar_1 = require("app/components/performance/waterfall/rowBar");
const utils_1 = require("app/components/performance/waterfall/utils");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const userMisery_1 = (0, tslib_1.__importDefault)(require("app/components/userMisery"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const analytics_1 = require("app/utils/analytics");
const fields_1 = require("app/utils/discover/fields");
const events_1 = require("app/utils/events");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const filter_1 = require("app/views/performance/transactionSummary/filter");
const arrayValue_1 = (0, tslib_1.__importDefault)(require("./arrayValue"));
const styles_1 = require("./styles");
const teamKeyTransactionField_1 = (0, tslib_1.__importDefault)(require("./teamKeyTransactionField"));
const EmptyValueContainer = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
`;
const emptyValue = <EmptyValueContainer>{(0, locale_1.t)('n/a')}</EmptyValueContainer>;
/**
 * A mapping of field types to their rendering function.
 * This mapping is used when a field is not defined in SPECIAL_FIELDS
 * and the field is not being coerced to a link.
 *
 * This mapping should match the output sentry.utils.snuba:get_json_type
 */
const FIELD_FORMATTERS = {
    boolean: {
        isSortable: true,
        renderFunc: (field, data) => {
            const value = data[field] ? (0, locale_1.t)('true') : (0, locale_1.t)('false');
            return <styles_1.Container>{value}</styles_1.Container>;
        },
    },
    date: {
        isSortable: true,
        renderFunc: (field, data) => (<styles_1.Container>
        {data[field]
                ? (0, getDynamicText_1.default)({
                    value: <styles_1.FieldDateTime date={data[field]}/>,
                    fixed: 'timestamp',
                })
                : emptyValue}
      </styles_1.Container>),
    },
    duration: {
        isSortable: true,
        renderFunc: (field, data) => (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? (<duration_1.default seconds={data[field] / 1000} fixedDigits={2} abbreviation/>) : (emptyValue)}
      </styles_1.NumberContainer>),
    },
    integer: {
        isSortable: true,
        renderFunc: (field, data) => (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? <count_1.default value={data[field]}/> : emptyValue}
      </styles_1.NumberContainer>),
    },
    number: {
        isSortable: true,
        renderFunc: (field, data) => (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? (0, formatters_1.formatFloat)(data[field], 4) : emptyValue}
      </styles_1.NumberContainer>),
    },
    percentage: {
        isSortable: true,
        renderFunc: (field, data) => (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? (0, formatters_1.formatPercentage)(data[field]) : emptyValue}
      </styles_1.NumberContainer>),
    },
    string: {
        isSortable: true,
        renderFunc: (field, data) => {
            // Some fields have long arrays in them, only show the tail of the data.
            const value = Array.isArray(data[field])
                ? data[field].slice(-1)
                : (0, utils_2.defined)(data[field])
                    ? data[field]
                    : emptyValue;
            if ((0, utils_2.isUrl)(value)) {
                return (<styles_1.Container>
            <externalLink_1.default href={value} data-test-id="group-tag-url">
              {value}
            </externalLink_1.default>
          </styles_1.Container>);
            }
            return <styles_1.Container>{value}</styles_1.Container>;
        },
    },
    array: {
        isSortable: true,
        renderFunc: (field, data) => {
            const value = Array.isArray(data[field]) ? data[field] : [data[field]];
            return <arrayValue_1.default value={value}/>;
        },
    },
};
/**
 * "Special fields" either do not map 1:1 to an single column in the event database,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
const SPECIAL_FIELDS = {
    id: {
        sortField: 'id',
        renderFunc: data => {
            const id = data === null || data === void 0 ? void 0 : data.id;
            if (typeof id !== 'string') {
                return null;
            }
            return <styles_1.Container>{(0, events_1.getShortEventId)(id)}</styles_1.Container>;
        },
    },
    trace: {
        sortField: 'trace',
        renderFunc: data => {
            const id = data === null || data === void 0 ? void 0 : data.trace;
            if (typeof id !== 'string') {
                return null;
            }
            return <styles_1.Container>{(0, events_1.getShortEventId)(id)}</styles_1.Container>;
        },
    },
    'issue.id': {
        sortField: 'issue.id',
        renderFunc: (data, { organization }) => {
            const target = {
                pathname: `/organizations/${organization.slug}/issues/${data['issue.id']}/`,
            };
            return (<styles_1.Container>
          <styles_1.OverflowLink to={target} aria-label={data['issue.id']}>
            {data['issue.id']}
          </styles_1.OverflowLink>
        </styles_1.Container>);
        },
    },
    issue: {
        sortField: null,
        renderFunc: (data, { organization }) => {
            const issueID = data['issue.id'];
            if (!issueID) {
                return (<styles_1.Container>
            <styles_1.FieldShortId shortId={`${data.issue}`}/>
          </styles_1.Container>);
            }
            const target = {
                pathname: `/organizations/${organization.slug}/issues/${issueID}/`,
            };
            return (<styles_1.Container>
          <styles_1.OverflowLink to={target} aria-label={issueID}>
            <styles_1.FieldShortId shortId={`${data.issue}`}/>
          </styles_1.OverflowLink>
        </styles_1.Container>);
        },
    },
    project: {
        sortField: 'project',
        renderFunc: (data, { organization }) => {
            return (<styles_1.Container>
          <projects_1.default orgId={organization.slug} slugs={[data.project]}>
            {({ projects }) => {
                    const project = projects.find(p => p.slug === data.project);
                    return (<projectBadge_1.default project={project ? project : { slug: data.project }} avatarSize={16}/>);
                }}
          </projects_1.default>
        </styles_1.Container>);
        },
    },
    user: {
        sortField: 'user',
        renderFunc: data => {
            if (data.user) {
                const [key, value] = data.user.split(':');
                const userObj = {
                    id: '',
                    name: '',
                    email: '',
                    username: '',
                    ip_address: '',
                };
                userObj[key] = value;
                const badge = <userBadge_1.default user={userObj} hideEmail avatarSize={16}/>;
                return <styles_1.Container>{badge}</styles_1.Container>;
            }
            return <styles_1.Container>{emptyValue}</styles_1.Container>;
        },
    },
    'user.display': {
        sortField: 'user.display',
        renderFunc: data => {
            if (data['user.display']) {
                const userObj = {
                    id: '',
                    name: data['user.display'],
                    email: '',
                    username: '',
                    ip_address: '',
                };
                const badge = <userBadge_1.default user={userObj} hideEmail avatarSize={16}/>;
                return <styles_1.Container>{badge}</styles_1.Container>;
            }
            return <styles_1.Container>{emptyValue}</styles_1.Container>;
        },
    },
    'count_unique(user)': {
        sortField: 'count_unique(user)',
        renderFunc: data => {
            const count = data.count_unique_user;
            if (typeof count === 'number') {
                return (<styles_1.FlexContainer>
            <styles_1.NumberContainer>
              <count_1.default value={count}/>
            </styles_1.NumberContainer>
            <styles_1.UserIcon size="20"/>
          </styles_1.FlexContainer>);
            }
            return <styles_1.Container>{emptyValue}</styles_1.Container>;
        },
    },
    release: {
        sortField: 'release',
        renderFunc: data => data.release ? (<styles_1.VersionContainer>
          <version_1.default version={data.release} anchor={false} tooltipRawVersion truncate/>
        </styles_1.VersionContainer>) : (<styles_1.Container>{emptyValue}</styles_1.Container>),
    },
    'error.handled': {
        sortField: 'error.handled',
        renderFunc: data => {
            const values = data['error.handled'];
            // Transactions will have null, and default events have no handled attributes.
            if (values === null || (values === null || values === void 0 ? void 0 : values.length) === 0) {
                return <styles_1.Container>{emptyValue}</styles_1.Container>;
            }
            const value = Array.isArray(values) ? values.slice(-1)[0] : values;
            return <styles_1.Container>{[1, null].includes(value) ? 'true' : 'false'}</styles_1.Container>;
        },
    },
    team_key_transaction: {
        sortField: null,
        renderFunc: (data, { organization }) => {
            var _a;
            return (<styles_1.Container>
        <teamKeyTransactionField_1.default isKeyTransaction={((_a = data.team_key_transaction) !== null && _a !== void 0 ? _a : 0) !== 0} organization={organization} projectSlug={data.project} transactionName={data.transaction}/>
      </styles_1.Container>);
        },
    },
    'trend_percentage()': {
        sortField: 'trend_percentage()',
        renderFunc: data => (<styles_1.NumberContainer>
        {typeof data.trend_percentage === 'number'
                ? (0, formatters_1.formatPercentage)(data.trend_percentage - 1)
                : emptyValue}
      </styles_1.NumberContainer>),
    },
    'timestamp.to_hour': {
        sortField: 'timestamp.to_hour',
        renderFunc: data => (<styles_1.Container>
        {(0, getDynamicText_1.default)({
                value: <styles_1.FieldDateTime date={data['timestamp.to_hour']} format="lll z"/>,
                fixed: 'timestamp.to_hour',
            })}
      </styles_1.Container>),
    },
    'timestamp.to_day': {
        sortField: 'timestamp.to_day',
        renderFunc: data => (<styles_1.Container>
        {(0, getDynamicText_1.default)({
                value: <styles_1.FieldDateTime date={data['timestamp.to_day']} dateOnly utc/>,
                fixed: 'timestamp.to_day',
            })}
      </styles_1.Container>),
    },
};
/**
 * "Special functions" are functions whose values either do not map 1:1 to a single column,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
const SPECIAL_FUNCTIONS = {
    user_misery: fieldName => data => {
        const userMiseryField = fieldName;
        if (!(userMiseryField in data)) {
            return <styles_1.NumberContainer>{emptyValue}</styles_1.NumberContainer>;
        }
        const userMisery = data[userMiseryField];
        if (userMisery === null || isNaN(userMisery)) {
            return <styles_1.NumberContainer>{emptyValue}</styles_1.NumberContainer>;
        }
        const projectThresholdConfig = 'project_threshold_config';
        let countMiserableUserField = '';
        let miseryLimit = parseInt(userMiseryField.split('_').pop() || '', 10);
        if (isNaN(miseryLimit)) {
            countMiserableUserField = 'count_miserable_user';
            if (projectThresholdConfig in data) {
                miseryLimit = data[projectThresholdConfig][1];
            }
            else {
                miseryLimit = undefined;
            }
        }
        else {
            countMiserableUserField = `count_miserable_user_${miseryLimit}`;
        }
        const uniqueUsers = data.count_unique_user;
        let miserableUsers;
        if (countMiserableUserField in data) {
            const countMiserableMiseryLimit = parseInt(countMiserableUserField.split('_').pop() || '', 10);
            miserableUsers =
                countMiserableMiseryLimit === miseryLimit ||
                    (isNaN(countMiserableMiseryLimit) && projectThresholdConfig)
                    ? data[countMiserableUserField]
                    : undefined;
        }
        return (<styles_1.BarContainer>
        <userMisery_1.default bars={10} barHeight={20} miseryLimit={miseryLimit} totalUsers={uniqueUsers} userMisery={userMisery} miserableUsers={miserableUsers}/>
      </styles_1.BarContainer>);
    },
};
/**
 * Get the sort field name for a given field if it is special or fallback
 * to the generic type formatter.
 */
function getSortField(field, tableMeta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].sortField;
    }
    if (!tableMeta) {
        return field;
    }
    if ((0, fields_1.isEquation)(field)) {
        return field;
    }
    for (const alias in fields_1.AGGREGATIONS) {
        if (field.startsWith(alias)) {
            return fields_1.AGGREGATIONS[alias].isSortable ? field : null;
        }
    }
    const fieldType = tableMeta[field];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return FIELD_FORMATTERS[fieldType].isSortable
            ? field
            : null;
    }
    return null;
}
exports.getSortField = getSortField;
const isDurationValue = (data, field) => {
    return field in data && typeof data[field] === 'number';
};
const spanOperationRelativeBreakdownRenderer = (data, { location, organization, eventView }) => {
    var _a, _b;
    const sumOfSpanTime = fields_1.SPAN_OP_BREAKDOWN_FIELDS.reduce((prev, curr) => (isDurationValue(data, curr) ? prev + data[curr] : prev), 0);
    const cumulativeSpanOpBreakdown = Math.max(sumOfSpanTime, data['transaction.duration']);
    if (fields_1.SPAN_OP_BREAKDOWN_FIELDS.every(field => !isDurationValue(data, field)) ||
        cumulativeSpanOpBreakdown === 0) {
        return FIELD_FORMATTERS.duration.renderFunc(fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD, data);
    }
    let otherPercentage = 1;
    let orderedSpanOpsBreakdownFields;
    const sortingOnField = (_b = (_a = eventView === null || eventView === void 0 ? void 0 : eventView.sorts) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.field;
    if (sortingOnField && fields_1.SPAN_OP_BREAKDOWN_FIELDS.includes(sortingOnField)) {
        orderedSpanOpsBreakdownFields = [
            sortingOnField,
            ...fields_1.SPAN_OP_BREAKDOWN_FIELDS.filter(op => op !== sortingOnField),
        ];
    }
    else {
        orderedSpanOpsBreakdownFields = fields_1.SPAN_OP_BREAKDOWN_FIELDS;
    }
    return (<RelativeOpsBreakdown>
      {orderedSpanOpsBreakdownFields.map(field => {
            var _a;
            if (!isDurationValue(data, field)) {
                return null;
            }
            const operationName = (_a = (0, fields_1.getSpanOperationName)(field)) !== null && _a !== void 0 ? _a : 'op';
            const spanOpDuration = data[field];
            const widthPercentage = spanOpDuration / cumulativeSpanOpBreakdown;
            otherPercentage = otherPercentage - widthPercentage;
            if (widthPercentage === 0) {
                return null;
            }
            return (<div key={operationName} style={{ width: (0, utils_1.toPercent)(widthPercentage || 0) }}>
            <tooltip_1.default title={<div>
                  <div>{operationName}</div>
                  <div>
                    <duration_1.default seconds={spanOpDuration / 1000} fixedDigits={2} abbreviation/>
                  </div>
                </div>} containerDisplayMode="block">
              <RectangleRelativeOpsBreakdown spanBarHatch={false} style={{
                    backgroundColor: (0, utils_1.pickBarColor)(operationName),
                    cursor: 'pointer',
                }} onClick={event => {
                    event.stopPropagation();
                    const filter = (0, filter_1.stringToFilter)(operationName);
                    if (filter === filter_1.SpanOperationBreakdownFilter.None) {
                        return;
                    }
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventName: 'Performance Views: Select Relative Breakdown',
                        eventKey: 'performance_views.relative_breakdown.selection',
                        organization_id: parseInt(organization.id, 10),
                        action: filter,
                    });
                    react_router_1.browserHistory.push({
                        pathname: location.pathname,
                        query: Object.assign(Object.assign({}, location.query), (0, filter_1.filterToLocationQuery)(filter)),
                    });
                }}/>
            </tooltip_1.default>
          </div>);
        })}
      <div key="other" style={{ width: (0, utils_1.toPercent)(otherPercentage || 0) }}>
        <tooltip_1.default title={<div>{(0, locale_1.t)('Other')}</div>} containerDisplayMode="block">
          <OtherRelativeOpsBreakdown spanBarHatch={false}/>
        </tooltip_1.default>
      </div>
    </RelativeOpsBreakdown>);
};
const RelativeOpsBreakdown = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
`;
const RectangleRelativeOpsBreakdown = (0, styled_1.default)(rowBar_1.RowRectangle) `
  position: relative;
  width: 100%;
`;
const OtherRelativeOpsBreakdown = (0, styled_1.default)(RectangleRelativeOpsBreakdown) `
  background-color: ${p => p.theme.gray100};
`;
/**
 * Get the field renderer for the named field and metadata
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
function getFieldRenderer(field, meta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].renderFunc;
    }
    if ((0, fields_1.isRelativeSpanOperationBreakdownField)(field)) {
        return spanOperationRelativeBreakdownRenderer;
    }
    const fieldName = (0, fields_1.getAggregateAlias)(field);
    const fieldType = meta[fieldName];
    for (const alias in SPECIAL_FUNCTIONS) {
        if (fieldName.startsWith(alias)) {
            return SPECIAL_FUNCTIONS[alias](fieldName);
        }
    }
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return (0, partial_1.default)(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return (0, partial_1.default)(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
exports.getFieldRenderer = getFieldRenderer;
/**
 * Get the field renderer for the named field only based on its type from the given
 * metadata.
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
function getFieldFormatter(field, meta) {
    const fieldName = (0, fields_1.getAggregateAlias)(field);
    const fieldType = meta[fieldName];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return (0, partial_1.default)(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return (0, partial_1.default)(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
exports.getFieldFormatter = getFieldFormatter;
//# sourceMappingURL=fieldRenderers.jsx.map