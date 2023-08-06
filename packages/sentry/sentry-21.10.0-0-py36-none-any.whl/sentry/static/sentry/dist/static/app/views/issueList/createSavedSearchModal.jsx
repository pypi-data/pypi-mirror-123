Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const indicator_1 = require("app/actionCreators/indicator");
const savedSearches_1 = require("app/actionCreators/savedSearches");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const forms_1 = require("app/views/settings/components/forms");
const utils_1 = require("./utils");
const DEFAULT_SORT_OPTIONS = [
    utils_1.IssueSortOptions.DATE,
    utils_1.IssueSortOptions.NEW,
    utils_1.IssueSortOptions.FREQ,
    utils_1.IssueSortOptions.PRIORITY,
    utils_1.IssueSortOptions.USER,
];
class CreateSavedSearchModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isSaving: false,
            error: null,
        };
        this.handleSubmit = (data, onSubmitSuccess, onSubmitError, event) => {
            const { api, organization } = this.props;
            const sort = this.validateSortOption(data.sort);
            event.preventDefault();
            this.setState({ isSaving: true });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving Changes'));
            (0, savedSearches_1.createSavedSearch)(api, organization.slug, data.name, data.query, sort)
                .then(_data => {
                this.props.closeModal();
                this.setState({
                    error: null,
                    isSaving: false,
                });
                (0, indicator_1.clearIndicators)();
                onSubmitSuccess(data);
            })
                .catch(err => {
                let error = (0, locale_1.t)('Unable to save your changes.');
                if (err.responseJSON && err.responseJSON.detail) {
                    error = err.responseJSON.detail;
                }
                this.setState({
                    error,
                    isSaving: false,
                });
                (0, indicator_1.clearIndicators)();
                onSubmitError(error);
            });
        };
    }
    /** Handle "date added" sort not being available for saved searches */
    validateSortOption(sort) {
        if (this.sortOptions().find(option => option === sort)) {
            return sort;
        }
        return utils_1.IssueSortOptions.DATE;
    }
    sortOptions() {
        var _a;
        const { organization } = this.props;
        const options = [...DEFAULT_SORT_OPTIONS];
        if ((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('issue-list-trend-sort')) {
            options.push(utils_1.IssueSortOptions.TREND);
        }
        return options;
    }
    render() {
        const { error } = this.state;
        const { Header, Body, closeModal, query, sort } = this.props;
        const sortOptions = this.sortOptions().map(sortOption => ({
            value: sortOption,
            label: (0, utils_1.getSortLabel)(sortOption),
        }));
        const initialData = {
            name: '',
            query,
            sort: this.validateSortOption(sort),
        };
        return (<forms_1.Form onSubmit={this.handleSubmit} onCancel={closeModal} saveOnBlur={false} initialData={initialData} submitLabel={(0, locale_1.t)('Save')}>
        <Header>
          <h4>{(0, locale_1.t)('Save Current Search')}</h4>
        </Header>

        <Body>
          {this.state.error && <alert_1.default type="error">{error}</alert_1.default>}

          <p>{(0, locale_1.t)('All team members will now have access to this search.')}</p>
          <forms_1.TextField key="name" name="name" label={(0, locale_1.t)('Name')} placeholder="e.g. My Search Results" inline={false} stacked flexibleControlStateSize required/>
          <forms_1.TextField key="query" name="query" label={(0, locale_1.t)('Query')} inline={false} stacked flexibleControlStateSize required/>
          <forms_1.SelectField key="sort" name="sort" label={(0, locale_1.t)('Sort By')} options={sortOptions} required clearable={false} inline={false} stacked flexibleControlStateSize/>
        </Body>
      </forms_1.Form>);
    }
}
exports.default = (0, withApi_1.default)(CreateSavedSearchModal);
//# sourceMappingURL=createSavedSearchModal.jsx.map