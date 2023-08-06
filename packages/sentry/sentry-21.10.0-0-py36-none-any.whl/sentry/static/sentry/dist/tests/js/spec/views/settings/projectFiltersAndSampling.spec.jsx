Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const utils_1 = require("sentry-test/utils");
const globalModal_1 = (0, tslib_1.__importDefault)(require("app/components/globalModal"));
const filtersAndSampling_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/filtersAndSampling"));
const utils_2 = require("app/views/settings/project/filtersAndSampling/utils");
describe('Filters and Sampling', function () {
    const commonConditionCategories = [
        'Release',
        'Environment',
        'User Id',
        'User Segment',
        'Browser Extensions',
        'Localhost',
        'Legacy Browser',
        'Web Crawlers',
        'IP Address',
        'Content Security Policy',
        'Error Message',
        'Transaction',
    ];
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/projects/org-slug/project-slug/',
        method: 'GET',
        // @ts-expect-error
        body: TestStubs.Project(),
    });
    function renderComponent(withModal = true) {
        const { organization, project } = (0, initializeOrg_1.initializeOrg)({
            organization: { features: ['filters-and-sampling'] },
        });
        return (0, reactTestingLibrary_1.mountWithTheme)(<react_1.Fragment>
        {withModal && <globalModal_1.default />}
        <filtersAndSampling_1.default organization={organization} project={project}/>
      </react_1.Fragment>);
    }
    function renderModal(actionElement, takeScreenshot = false) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // Open Modal
            reactTestingLibrary_1.fireEvent.click(actionElement);
            const dialog = yield reactTestingLibrary_1.screen.findByRole('dialog');
            expect(dialog).toBeInTheDocument();
            if (takeScreenshot) {
                expect(dialog).toSnapshot();
            }
            return (0, reactTestingLibrary_1.within)(dialog);
        });
    }
    describe('renders', function () {
        it('empty', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const component = renderComponent(false);
                const { container } = component;
                // Title
                expect(reactTestingLibrary_1.screen.getByText('Filters & Sampling')).toBeTruthy();
                // Error rules container
                expect(yield (0, utils_1.findByTextContent)(reactTestingLibrary_1.screen, 'Manage the inbound data you want to store. To change the sampling rate or rate limits, update your SDK configuration. The rules added below will apply on top of your SDK configuration. Any new rule may take a few minutes to propagate.')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByRole('link', {
                    name: 'update your SDK configuration',
                })).toHaveAttribute('href', utils_2.DYNAMIC_SAMPLING_DOC_LINK);
                expect(reactTestingLibrary_1.screen.getByText('There are no error rules to display')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByText('Add error rule')).toBeTruthy();
                // Transaction traces and individual transactions rules container
                expect(reactTestingLibrary_1.screen.getByText('Rules for traces should precede rules for individual transactions.')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByText('There are no transaction rules to display')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByText('Add transaction rule')).toBeTruthy();
                const readDocsButtonLinks = reactTestingLibrary_1.screen.queryAllByRole('button', {
                    name: 'Read the docs',
                });
                expect(readDocsButtonLinks).toHaveLength(2);
                for (const readDocsButtonLink of readDocsButtonLinks) {
                    expect(readDocsButtonLink).toHaveAttribute('href', utils_2.DYNAMIC_SAMPLING_DOC_LINK);
                }
                expect(reactTestingLibrary_1.screen.queryAllByText('Type')).toHaveLength(2);
                expect(reactTestingLibrary_1.screen.queryAllByText('Conditions')).toHaveLength(2);
                expect(reactTestingLibrary_1.screen.queryAllByText('Rate')).toHaveLength(2);
                expect(container).toSnapshot();
            });
        });
        it('with rules', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'GET',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.2,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 39,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'transaction',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'custom',
                                                name: 'event.legacy_browser',
                                                value: [
                                                    'ie_pre_9',
                                                    'ie9',
                                                    'ie10',
                                                    'ie11',
                                                    'safari_pre_6',
                                                    'opera_pre_15',
                                                    'opera_mini_pre_8',
                                                    'android_pre_4',
                                                ],
                                            },
                                        ],
                                    },
                                    id: 42,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                const component = renderComponent(false);
                const { container } = component;
                // Title
                expect(reactTestingLibrary_1.screen.getByText('Filters & Sampling')).toBeTruthy();
                // Error rules container
                expect(yield (0, utils_1.findByTextContent)(reactTestingLibrary_1.screen, 'Manage the inbound data you want to store. To change the sampling rate or rate limits, update your SDK configuration. The rules added below will apply on top of your SDK configuration. Any new rule may take a few minutes to propagate.')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByRole('link', {
                    name: 'update your SDK configuration',
                })).toHaveAttribute('href', utils_2.DYNAMIC_SAMPLING_DOC_LINK);
                expect(reactTestingLibrary_1.screen.queryByText('There are no error rules to display')).toBeFalsy();
                const errorRules = reactTestingLibrary_1.screen.queryAllByText('Errors only');
                expect(errorRules).toHaveLength(1);
                expect(reactTestingLibrary_1.screen.getByText('Add error rule')).toBeTruthy();
                // Transaction traces and individual transactions rules container
                expect(reactTestingLibrary_1.screen.getByText('Rules for traces should precede rules for individual transactions.')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                const transactionTraceRules = reactTestingLibrary_1.screen.queryAllByText('Transaction traces');
                expect(transactionTraceRules).toHaveLength(1);
                const individualTransactionRules = reactTestingLibrary_1.screen.queryAllByText('Individual transactions');
                expect(individualTransactionRules).toHaveLength(1);
                expect(reactTestingLibrary_1.screen.getByText('Add transaction rule')).toBeTruthy();
                const readDocsButtonLinks = reactTestingLibrary_1.screen.queryAllByRole('button', {
                    name: 'Read the docs',
                });
                expect(readDocsButtonLinks).toHaveLength(2);
                for (const readDocsButtonLink of readDocsButtonLinks) {
                    expect(readDocsButtonLink).toHaveAttribute('href', utils_2.DYNAMIC_SAMPLING_DOC_LINK);
                }
                expect(reactTestingLibrary_1.screen.queryAllByText('Type')).toHaveLength(2);
                expect(reactTestingLibrary_1.screen.queryAllByText('Conditions')).toHaveLength(2);
                expect(reactTestingLibrary_1.screen.queryAllByText('Rate')).toHaveLength(2);
                expect(container).toSnapshot();
            });
        });
    });
    describe('edit rules', function () {
        it('error rule', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'GET',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.1,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1*'],
                                            },
                                        ],
                                    },
                                    id: 39,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'PUT',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.5,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['[I3].[0-9]'],
                                            },
                                        ],
                                    },
                                    id: 44,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/organizations/org-slug/tags/release/values/',
                    method: 'GET',
                    body: [{ value: '[I3].[0-9]' }],
                });
                renderComponent();
                // Error rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no error rules to display')).toBeFalsy();
                const errorRules = reactTestingLibrary_1.screen.queryAllByText('Errors only');
                expect(errorRules).toHaveLength(1);
                // Transaction traces and individual transactions rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                const transactionTraceRules = reactTestingLibrary_1.screen.queryAllByText('Transaction traces');
                expect(transactionTraceRules).toHaveLength(1);
                const editRuleButtons = reactTestingLibrary_1.screen.queryAllByLabelText('Edit Rule');
                expect(editRuleButtons).toHaveLength(2);
                // Open rule modal - edit error rule
                const modal = yield renderModal(editRuleButtons[0]);
                // Modal content
                expect(modal.getByText('Edit Error Sampling Rule')).toBeTruthy();
                expect(modal.queryByText('Tracing')).toBeFalsy();
                // Release Field
                yield modal.findByTestId('autocomplete-release');
                const releaseField = modal.getByTestId('autocomplete-release');
                expect(releaseField).toBeTruthy();
                // Release field is not empty
                const releaseFieldValues = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('multivalue');
                expect(releaseFieldValues).toHaveLength(1);
                expect(releaseFieldValues[0].textContent).toEqual('1*');
                // Button is enabled - meaning the form is valid
                const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButton).toBeTruthy();
                expect(saveRuleButton).toBeEnabled();
                // Sample rate field
                const sampleRateField = modal.getByPlaceholderText('\u0025');
                expect(sampleRateField).toBeTruthy();
                // Sample rate is not empty
                expect(sampleRateField).toHaveValue(10);
                const releaseFieldInput = (0, reactTestingLibrary_1.within)(releaseField).getByLabelText('Search or add a release');
                // Clear release field
                reactTestingLibrary_1.fireEvent.keyDown(releaseFieldInput, { key: 'Backspace' });
                // Release field is now empty
                const newReleaseFieldValues = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('multivalue');
                expect(newReleaseFieldValues).toHaveLength(0);
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeDisabled();
                // Type into realease field
                reactTestingLibrary_1.fireEvent.change((0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).getByLabelText('Search or add a release'), {
                    target: { value: '[I3].[0-9]' },
                });
                // Autocomplete suggests options
                const autocompleteOptions = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('option');
                expect(autocompleteOptions).toHaveLength(1);
                expect(autocompleteOptions[0].textContent).toEqual('[I3].[0-9]');
                // Click on the suggested option
                reactTestingLibrary_1.fireEvent.click(autocompleteOptions[0]);
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeEnabled();
                // Clear sample rate field
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: null } });
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeDisabled();
                // Update sample rate field
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 50 } });
                // Save button is now enabled
                const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButtonEnabled).toBeEnabled();
                // Click on save button
                reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                // Modal will close
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Edit Error Sampling Rule'));
                // Error rules panel is updated
                expect(errorRules).toHaveLength(1);
                expect(reactTestingLibrary_1.screen.getByText('Errors only')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.queryAllByText('Release')).toHaveLength(2);
                // Old values
                expect(reactTestingLibrary_1.screen.queryByText('1*')).toBeFalsy();
                expect(reactTestingLibrary_1.screen.queryByText('10%')).toBeFalsy();
                // New values
                expect(reactTestingLibrary_1.screen.getByText('[I3].[0-9]')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByText('50%')).toBeTruthy();
            });
        });
        it('transaction trace rule', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'GET',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.1,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1*'],
                                            },
                                        ],
                                    },
                                    id: 39,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'PUT',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.1,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1*'],
                                            },
                                        ],
                                    },
                                    id: 44,
                                },
                                {
                                    sampleRate: 0.6,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['[0-9]'],
                                            },
                                        ],
                                    },
                                    id: 45,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/organizations/org-slug/tags/release/values/',
                    method: 'GET',
                    body: [{ value: '[0-9]' }],
                });
                renderComponent();
                // Error rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no error rules to display')).toBeFalsy();
                const errorRules = reactTestingLibrary_1.screen.queryAllByText('Errors only');
                expect(errorRules).toHaveLength(1);
                // Transaction traces and individual transactions rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                const transactionTraceRules = reactTestingLibrary_1.screen.queryAllByText('Transaction traces');
                expect(transactionTraceRules).toHaveLength(1);
                const editRuleButtons = reactTestingLibrary_1.screen.queryAllByLabelText('Edit Rule');
                expect(editRuleButtons).toHaveLength(2);
                // Open rule modal - edit transaction rule
                const modal = yield renderModal(editRuleButtons[1]);
                // Modal content
                expect(modal.getByText('Edit Transaction Sampling Rule')).toBeTruthy();
                expect(modal.queryByText('Tracing')).toBeTruthy();
                expect(modal.getByRole('checkbox')).toBeChecked();
                // Release Field
                yield modal.findByTestId('autocomplete-release');
                const releaseField = modal.getByTestId('autocomplete-release');
                expect(releaseField).toBeTruthy();
                // Release field is not empty
                const releaseFieldValues = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('multivalue');
                expect(releaseFieldValues).toHaveLength(1);
                expect(releaseFieldValues[0].textContent).toEqual('1.2.3');
                // Button is enabled - meaning the form is valid
                const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButton).toBeTruthy();
                expect(saveRuleButton).toBeEnabled();
                // Sample rate field
                const sampleRateField = modal.getByPlaceholderText('\u0025');
                expect(sampleRateField).toBeTruthy();
                // Sample rate is not empty
                expect(sampleRateField).toHaveValue(20);
                const releaseFieldInput = (0, reactTestingLibrary_1.within)(releaseField).getByLabelText('Search or add a release');
                // Clear release field
                reactTestingLibrary_1.fireEvent.keyDown(releaseFieldInput, { key: 'Backspace' });
                // Release field is now empty
                const newReleaseFieldValues = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('multivalue');
                expect(newReleaseFieldValues).toHaveLength(0);
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeDisabled();
                // Type into realease field
                reactTestingLibrary_1.fireEvent.change((0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).getByLabelText('Search or add a release'), {
                    target: { value: '[0-9]' },
                });
                // Autocomplete suggests options
                const autocompleteOptions = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('option');
                expect(autocompleteOptions).toHaveLength(1);
                expect(autocompleteOptions[0].textContent).toEqual('[0-9]');
                // Click on the suggested option
                reactTestingLibrary_1.fireEvent.click(autocompleteOptions[0]);
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeEnabled();
                // Clear sample rate field
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: null } });
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeDisabled();
                // Update sample rate field
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 60 } });
                // Save button is now enabled
                const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButtonEnabled).toBeEnabled();
                // Click on save button
                reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                // Modal will close
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Edit Transaction Sampling Rule'));
                // Error rules panel is updated
                expect(errorRules).toHaveLength(1);
                expect(reactTestingLibrary_1.screen.getByText('Transaction traces')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.queryAllByText('Release')).toHaveLength(2);
                // Old values
                expect(reactTestingLibrary_1.screen.queryByText('1.2.3')).toBeFalsy();
                expect(reactTestingLibrary_1.screen.queryByText('20%')).toBeFalsy();
                // New values
                expect(reactTestingLibrary_1.screen.getByText('[0-9]')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByText('60%')).toBeTruthy();
            });
        });
        it('individual transaction rule', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'GET',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.1,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1*'],
                                            },
                                        ],
                                    },
                                    id: 39,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'transaction',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'PUT',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.1,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1*'],
                                            },
                                        ],
                                    },
                                    id: 44,
                                },
                                {
                                    sampleRate: 0.6,
                                    type: 'transaction',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['[0-9]'],
                                            },
                                        ],
                                    },
                                    id: 45,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/organizations/org-slug/tags/release/values/',
                    method: 'GET',
                    body: [{ value: '[0-9]' }],
                });
                renderComponent();
                // Error rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no error rules to display')).toBeFalsy();
                const errorRules = reactTestingLibrary_1.screen.queryAllByText('Errors only');
                expect(errorRules).toHaveLength(1);
                // Transaction traces and individual transactions rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                const transactionTraceRules = reactTestingLibrary_1.screen.queryAllByText('Individual transactions');
                expect(transactionTraceRules).toHaveLength(1);
                const editRuleButtons = reactTestingLibrary_1.screen.queryAllByLabelText('Edit Rule');
                expect(editRuleButtons).toHaveLength(2);
                // Open rule modal - edit transaction rule
                const modal = yield renderModal(editRuleButtons[1]);
                // Modal content
                expect(modal.getByText('Edit Transaction Sampling Rule')).toBeTruthy();
                expect(modal.queryByText('Tracing')).toBeTruthy();
                expect(modal.getByRole('checkbox')).not.toBeChecked();
                // Release Field
                yield modal.findByTestId('autocomplete-release');
                const releaseField = modal.getByTestId('autocomplete-release');
                expect(releaseField).toBeTruthy();
                // Release field is not empty
                const releaseFieldValues = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('multivalue');
                expect(releaseFieldValues).toHaveLength(1);
                // Button is enabled - meaning the form is valid
                const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButton).toBeTruthy();
                expect(saveRuleButton).toBeEnabled();
                // Sample rate field
                const sampleRateField = modal.getByPlaceholderText('\u0025');
                expect(sampleRateField).toBeTruthy();
                // Sample rate is not empty
                expect(sampleRateField).toHaveValue(20);
                const releaseFieldInput = (0, reactTestingLibrary_1.within)(releaseField).getByLabelText('Search or add a release');
                // Clear release field
                reactTestingLibrary_1.fireEvent.keyDown(releaseFieldInput, { key: 'Backspace' });
                // Release field is now empty
                const newReleaseFieldValues = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('multivalue');
                expect(newReleaseFieldValues).toHaveLength(0);
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeDisabled();
                // Type into realease field
                reactTestingLibrary_1.fireEvent.change((0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).getByLabelText('Search or add a release'), {
                    target: { value: '[0-9]' },
                });
                // Autocomplete suggests options
                const autocompleteOptions = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('option');
                expect(autocompleteOptions).toHaveLength(1);
                expect(autocompleteOptions[0].textContent).toEqual('[0-9]');
                // Click on the suggested option
                reactTestingLibrary_1.fireEvent.click(autocompleteOptions[0]);
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeEnabled();
                // Clear sample rate field
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: null } });
                expect(modal.getByRole('button', { name: 'Save Rule' })).toBeDisabled();
                // Update sample rate field
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 60 } });
                // Save button is now enabled
                const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButtonEnabled).toBeEnabled();
                // Click on save button
                reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                // Modal will close
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Edit Transaction Sampling Rule'));
                // Error rules panel is updated
                expect(errorRules).toHaveLength(1);
                expect(reactTestingLibrary_1.screen.getByText('Individual transactions')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.queryAllByText('Release')).toHaveLength(2);
                // Old values
                expect(reactTestingLibrary_1.screen.queryByText('1.2.3')).toBeFalsy();
                expect(reactTestingLibrary_1.screen.queryByText('20%')).toBeFalsy();
                // New values
                expect(reactTestingLibrary_1.screen.getByText('[0-9]')).toBeTruthy();
                expect(reactTestingLibrary_1.screen.getByText('60%')).toBeTruthy();
            });
        });
    });
    describe('delete rules', function () {
        it('error rule', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'GET',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.2,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 39,
                                },
                                {
                                    sampleRate: 0.2,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'PUT',
                    // @ts-expect-error
                    body: TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.2,
                                    type: 'trace',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'trace.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 40,
                                },
                            ],
                            next_id: 43,
                        },
                    }),
                });
                renderComponent();
                // Error rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no error rules to display')).toBeFalsy();
                const errorRules = reactTestingLibrary_1.screen.queryAllByText('Errors only');
                expect(errorRules).toHaveLength(1);
                // Transaction traces and individual transactions rules container
                expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                const transactionTraceRules = reactTestingLibrary_1.screen.queryAllByText('Transaction traces');
                expect(transactionTraceRules).toHaveLength(1);
                const deleteRuleButtons = reactTestingLibrary_1.screen.queryAllByLabelText('Delete Rule');
                expect(deleteRuleButtons).toHaveLength(2);
                // Open deletion confirmation modal - delete error rule
                const modal = yield renderModal(deleteRuleButtons[0]);
                expect(modal.getByText('Are you sure you wish to delete this dynamic sampling rule?')).toBeTruthy();
                const modalActionButtons = modal.queryAllByRole('button');
                expect(modalActionButtons).toHaveLength(2);
                expect(modalActionButtons[0].textContent).toEqual('Cancel');
                expect(modalActionButtons[1].textContent).toEqual('Confirm');
                // Confirm deletion
                reactTestingLibrary_1.fireEvent.click(modalActionButtons[1]);
                // Confirmation modal will close
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Are you sure you wish to delete this dynamic sampling rule?'));
                // Error rules panel is updated
                expect(reactTestingLibrary_1.screen.queryByText('There are no error rules to display')).toBeTruthy();
                // There is still one transaction rule
                expect(transactionTraceRules).toHaveLength(1);
            });
        });
    });
    describe('error rule modal', function () {
        it('renders modal', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                renderComponent();
                // Open Modal
                const modal = yield renderModal(reactTestingLibrary_1.screen.getByText('Add error rule'), true);
                // Modal content
                expect(modal.getByText('Add Error Sampling Rule')).toBeTruthy();
                expect(modal.queryByText('Tracing')).toBeFalsy();
                expect(modal.getByText('Conditions')).toBeTruthy();
                expect(modal.getByText('Add Condition')).toBeTruthy();
                expect(modal.getByText('Apply sampling rate to all errors')).toBeTruthy();
                expect(modal.getByText('Sampling Rate \u0025')).toBeTruthy();
                expect(modal.getByPlaceholderText('\u0025')).toHaveValue(null);
                expect(modal.getByRole('button', { name: 'Cancel' })).toBeTruthy();
                const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButton).toBeTruthy();
                expect(saveRuleButton).toBeDisabled();
                // Close Modal
                reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByLabelText('Close Modal'));
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Add Error Sampling Rule'));
            });
        });
        it('condition options', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                renderComponent();
                // Open Modal
                const modal = yield renderModal(reactTestingLibrary_1.screen.getByText('Add error rule'));
                // Click on 'Add condition'
                reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                // Autocomplete
                const autoCompleteList = yield reactTestingLibrary_1.screen.findByTestId('autocomplete-list');
                expect(autoCompleteList).toBeInTheDocument();
                // Condition Options
                const conditionOptions = modal.queryAllByRole('presentation');
                expect(conditionOptions).toHaveLength(commonConditionCategories.length);
                for (const conditionOptionIndex in conditionOptions) {
                    expect(conditionOptions[conditionOptionIndex].textContent).toEqual(commonConditionCategories[conditionOptionIndex]);
                }
                // Close Modal
                reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByLabelText('Close Modal'));
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Add Error Sampling Rule'));
            });
        });
        it('save rule', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/projects/org-slug/project-slug/',
                    method: 'PUT',
                    body: 
                    // @ts-expect-error
                    TestStubs.Project({
                        dynamicSampling: {
                            rules: [
                                {
                                    sampleRate: 0.2,
                                    type: 'error',
                                    condition: {
                                        op: 'and',
                                        inner: [
                                            {
                                                op: 'glob',
                                                name: 'event.release',
                                                value: ['1.2.3'],
                                            },
                                        ],
                                    },
                                    id: 39,
                                },
                            ],
                            next_id: 40,
                        },
                    }),
                });
                // @ts-expect-error
                MockApiClient.addMockResponse({
                    url: '/organizations/org-slug/tags/release/values/',
                    method: 'GET',
                    body: [{ value: '1.2.3' }],
                });
                const component = renderComponent();
                const { getByText, queryByText, queryAllByText } = component;
                // Open Modal
                const modal = yield renderModal(getByText('Add error rule'));
                // Click on 'Add condition'
                reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                // Autocomplete
                const autoCompleteList = yield modal.findByTestId('autocomplete-list');
                expect(autoCompleteList).toBeInTheDocument();
                // Condition Options
                const conditionOptions = modal.queryAllByRole('presentation');
                // Click on the first condition option
                reactTestingLibrary_1.fireEvent.click(conditionOptions[0]);
                // Release Field
                yield modal.findByTestId('autocomplete-release');
                const releaseField = modal.getByTestId('autocomplete-release');
                expect(releaseField).toBeTruthy();
                // Release field is empty
                const releaseFieldValues = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('multivalue');
                expect(releaseFieldValues).toHaveLength(0);
                // Type into realease field
                reactTestingLibrary_1.fireEvent.change((0, reactTestingLibrary_1.within)(releaseField).getByLabelText('Search or add a release'), {
                    target: { value: '1.2.3' },
                });
                // Autocomplete suggests options
                const autocompleteOptions = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('option');
                expect(autocompleteOptions).toHaveLength(1);
                expect(autocompleteOptions[0].textContent).toEqual('1.2.3');
                // Click on the suggested option
                reactTestingLibrary_1.fireEvent.click(autocompleteOptions[0]);
                // Button is still disabled
                const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButton).toBeTruthy();
                expect(saveRuleButton).toBeDisabled();
                // Fill sample rate field
                const sampleRateField = modal.getByPlaceholderText('\u0025');
                expect(sampleRateField).toBeTruthy();
                reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 20 } });
                // Save button is now enabled
                const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButtonEnabled).toBeEnabled();
                // Click on save button
                reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                // Modal will close
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => getByText('Add Error Sampling Rule'));
                // Error rules panel is updated
                expect(queryByText('There are no error rules to display')).toBeFalsy();
                const errorRules = queryAllByText('Errors only');
                expect(errorRules).toHaveLength(1);
                expect(getByText('Release')).toBeTruthy();
                expect(getByText('1.2.3')).toBeTruthy();
                expect(getByText('20%')).toBeTruthy();
            });
        });
    });
    describe('transaction rule modal', function () {
        const conditionTracingCategories = [
            'Release',
            'Environment',
            'User Id',
            'User Segment',
            'Transaction',
        ];
        it('renders modal', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                renderComponent();
                // Open Modal
                const modal = yield renderModal(reactTestingLibrary_1.screen.getByText('Add transaction rule'), true);
                // Modal content
                expect(modal.getByText('Add Transaction Sampling Rule')).toBeTruthy();
                expect(modal.getByText('Tracing')).toBeTruthy();
                expect(modal.getByRole('checkbox')).toBeChecked();
                expect(yield (0, utils_1.findByTextContent)(modal, 'Include all related transactions by trace ID. This can span across multiple projects. All related errors will remain. Learn more about tracing.')).toBeTruthy();
                expect(modal.getByRole('link', {
                    name: 'Learn more about tracing',
                })).toHaveAttribute('href', utils_2.DYNAMIC_SAMPLING_DOC_LINK);
                expect(modal.getByText('Conditions')).toBeTruthy();
                expect(modal.getByText('Add Condition')).toBeTruthy();
                expect(modal.getByText('Apply sampling rate to all transactions')).toBeTruthy();
                expect(modal.getByText('Sampling Rate \u0025')).toBeTruthy();
                expect(modal.getByPlaceholderText('\u0025')).toHaveValue(null);
                expect(modal.getByRole('button', { name: 'Cancel' })).toBeTruthy();
                const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                expect(saveRuleButton).toBeTruthy();
                expect(saveRuleButton).toBeDisabled();
                // Close Modal
                reactTestingLibrary_1.fireEvent.click(reactTestingLibrary_1.screen.getByLabelText('Close Modal'));
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Add Transaction Sampling Rule'));
            });
        });
        it('condition options', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const component = renderComponent();
                const { getByText, getByLabelText } = component;
                // Open Modal
                const modal = yield renderModal(getByText('Add transaction rule'));
                // Click on 'Add condition'
                reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                // Autocomplete
                const autoCompleteList = yield modal.findByTestId('autocomplete-list');
                expect(autoCompleteList).toBeInTheDocument();
                // Trancing Condition Options
                const conditionTracingOptions = modal.queryAllByRole('presentation');
                expect(conditionTracingOptions).toHaveLength(conditionTracingCategories.length);
                for (const conditionTracingOptionIndex in conditionTracingOptions) {
                    expect(conditionTracingOptions[conditionTracingOptionIndex].textContent).toEqual(conditionTracingCategories[conditionTracingOptionIndex]);
                }
                // Unchecked tracing checkbox
                reactTestingLibrary_1.fireEvent.click(modal.getByRole('checkbox'));
                // Click on 'Add condition'
                reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                // No Tracing Condition Options
                const conditionOptions = modal.queryAllByRole('presentation');
                expect(conditionOptions).toHaveLength(commonConditionCategories.length);
                for (const conditionOptionIndex in conditionOptions) {
                    expect(conditionOptions[conditionOptionIndex].textContent).toEqual(commonConditionCategories[conditionOptionIndex]);
                }
                // Close Modal
                reactTestingLibrary_1.fireEvent.click(getByLabelText('Close Modal'));
                yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => getByText('Add Transaction Sampling Rule'));
            });
        });
        describe('save rule', function () {
            it('transaction trace', function () {
                return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                    // @ts-expect-error
                    MockApiClient.addMockResponse({
                        url: '/projects/org-slug/project-slug/',
                        method: 'PUT',
                        body: 
                        // @ts-expect-error
                        TestStubs.Project({
                            dynamicSampling: {
                                rules: [
                                    {
                                        sampleRate: 0.2,
                                        type: 'trace',
                                        condition: {
                                            op: 'and',
                                            inner: [
                                                {
                                                    op: 'glob',
                                                    name: 'trace.release',
                                                    value: ['1.2.3'],
                                                },
                                            ],
                                        },
                                        id: 40,
                                    },
                                ],
                                next_id: 40,
                            },
                        }),
                    });
                    // @ts-expect-error
                    MockApiClient.addMockResponse({
                        url: '/organizations/org-slug/tags/release/values/',
                        method: 'GET',
                        body: [{ value: '1.2.3' }],
                    });
                    renderComponent();
                    // Open Modal
                    const modal = yield renderModal(reactTestingLibrary_1.screen.getByText('Add transaction rule'));
                    // Checked tracing checkbox
                    expect(modal.getByRole('checkbox')).toBeChecked();
                    // Click on 'Add condition'
                    reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                    // Autocomplete
                    const autoCompleteList = yield modal.findByTestId('autocomplete-list');
                    expect(autoCompleteList).toBeInTheDocument();
                    // Condition Options
                    const conditionOptions = modal.queryAllByRole('presentation');
                    // Click on the first condition option
                    reactTestingLibrary_1.fireEvent.click(conditionOptions[0]);
                    // Release Field
                    yield modal.findByTestId('autocomplete-release');
                    const releaseField = modal.getByTestId('autocomplete-release');
                    expect(releaseField).toBeTruthy();
                    // Release field is empty
                    const releaseFieldValues = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('multivalue');
                    expect(releaseFieldValues).toHaveLength(0);
                    // Type into realease field
                    reactTestingLibrary_1.fireEvent.change((0, reactTestingLibrary_1.within)(releaseField).getByLabelText('Search or add a release'), {
                        target: { value: '1.2.3' },
                    });
                    // Autocomplete suggests options
                    const autocompleteOptions = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('option');
                    expect(autocompleteOptions).toHaveLength(1);
                    expect(autocompleteOptions[0].textContent).toEqual('1.2.3');
                    // Click on the suggested option
                    reactTestingLibrary_1.fireEvent.click(autocompleteOptions[0]);
                    // Button is still disabled
                    const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                    expect(saveRuleButton).toBeTruthy();
                    expect(saveRuleButton).toBeDisabled();
                    // Fill sample rate field
                    const sampleRateField = modal.getByPlaceholderText('\u0025');
                    expect(sampleRateField).toBeTruthy();
                    reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 20 } });
                    // Save button is now enabled
                    const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                    expect(saveRuleButtonEnabled).toBeEnabled();
                    // Click on save button
                    reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                    // Modal will close
                    yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Add Transaction Sampling Rule'));
                    // Transaction rules panel is updated
                    expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                    const transactionTraceRules = reactTestingLibrary_1.screen.queryAllByText('Transaction traces');
                    expect(transactionTraceRules).toHaveLength(1);
                    expect(reactTestingLibrary_1.screen.getByText('Release')).toBeTruthy();
                    expect(reactTestingLibrary_1.screen.getByText('1.2.3')).toBeTruthy();
                    expect(reactTestingLibrary_1.screen.getByText('20%')).toBeTruthy();
                });
            });
            describe('individual transaction', function () {
                it('release', function () {
                    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: '/projects/org-slug/project-slug/',
                            method: 'PUT',
                            body: 
                            // @ts-expect-error
                            TestStubs.Project({
                                dynamicSampling: {
                                    rules: [
                                        {
                                            sampleRate: 0.2,
                                            type: 'transaction',
                                            condition: {
                                                op: 'and',
                                                inner: [
                                                    {
                                                        op: 'glob',
                                                        name: 'event.release',
                                                        value: ['1.2.3'],
                                                    },
                                                ],
                                            },
                                            id: 41,
                                        },
                                    ],
                                    next_id: 40,
                                },
                            }),
                        });
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: '/organizations/org-slug/tags/release/values/',
                            method: 'GET',
                            body: [{ value: '1.2.3' }],
                        });
                        renderComponent();
                        // Open Modal
                        const modal = yield renderModal(reactTestingLibrary_1.screen.getByText('Add transaction rule'));
                        // Unchecked tracing checkbox
                        reactTestingLibrary_1.fireEvent.click(modal.getByRole('checkbox'));
                        // Click on 'Add condition'
                        reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                        // Autocomplete
                        const autoCompleteList = yield reactTestingLibrary_1.screen.findByTestId('autocomplete-list');
                        expect(autoCompleteList).toBeInTheDocument();
                        // Condition Options
                        const conditionOptions = modal.queryAllByRole('presentation');
                        // Click on the first condition option
                        reactTestingLibrary_1.fireEvent.click(conditionOptions[0]);
                        // Release Field
                        yield modal.findByTestId('autocomplete-release');
                        const releaseField = modal.getByTestId('autocomplete-release');
                        expect(releaseField).toBeTruthy();
                        // Release field is empty
                        const releaseFieldValues = (0, reactTestingLibrary_1.within)(releaseField).queryAllByTestId('multivalue');
                        expect(releaseFieldValues).toHaveLength(0);
                        // Type into realease field
                        reactTestingLibrary_1.fireEvent.change((0, reactTestingLibrary_1.within)(releaseField).getByLabelText('Search or add a release'), {
                            target: { value: '1.2.3' },
                        });
                        // Autocomplete suggests options
                        const autocompleteOptions = (0, reactTestingLibrary_1.within)(modal.getByTestId('autocomplete-release')).queryAllByTestId('option');
                        expect(autocompleteOptions).toHaveLength(1);
                        expect(autocompleteOptions[0].textContent).toEqual('1.2.3');
                        // Click on the suggested option
                        reactTestingLibrary_1.fireEvent.click(autocompleteOptions[0]);
                        // Button is still disabled
                        const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                        expect(saveRuleButton).toBeTruthy();
                        expect(saveRuleButton).toBeDisabled();
                        // Fill sample rate field
                        const sampleRateField = modal.getByPlaceholderText('\u0025');
                        expect(sampleRateField).toBeTruthy();
                        reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 20 } });
                        // Save button is now enabled
                        const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                        expect(saveRuleButtonEnabled).toBeEnabled();
                        // Click on save button
                        reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                        // Modal will close
                        yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Add Transaction Sampling Rule'));
                        // Transaction rules panel is updated
                        expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                        const individualTransactionRules = reactTestingLibrary_1.screen.queryAllByText('Individual transactions');
                        expect(individualTransactionRules).toHaveLength(1);
                        expect(reactTestingLibrary_1.screen.getByText('Release')).toBeTruthy();
                        expect(reactTestingLibrary_1.screen.getByText('1.2.3')).toBeTruthy();
                        expect(reactTestingLibrary_1.screen.getByText('20%')).toBeTruthy();
                    });
                });
                it('legacy browser', function () {
                    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: '/projects/org-slug/project-slug/',
                            method: 'PUT',
                            body: 
                            // @ts-expect-error
                            TestStubs.Project({
                                dynamicSampling: {
                                    rules: [
                                        {
                                            sampleRate: 0.2,
                                            type: 'transaction',
                                            condition: {
                                                op: 'and',
                                                inner: [
                                                    {
                                                        op: 'custom',
                                                        name: 'event.legacy_browser',
                                                        value: [
                                                            'ie_pre_9',
                                                            'ie9',
                                                            'ie10',
                                                            'ie11',
                                                            'safari_pre_6',
                                                            'opera_pre_15',
                                                            'opera_mini_pre_8',
                                                            'android_pre_4',
                                                        ],
                                                    },
                                                ],
                                            },
                                            id: 42,
                                        },
                                    ],
                                    next_id: 40,
                                },
                            }),
                        });
                        renderComponent();
                        // Open Modal
                        const modal = yield renderModal(reactTestingLibrary_1.screen.getByText('Add transaction rule'));
                        const checkedCheckbox = modal.getByRole('checkbox');
                        // Checked tracing checkbox
                        expect(checkedCheckbox).toBeChecked();
                        // Uncheck tracing checkbox
                        reactTestingLibrary_1.fireEvent.click(checkedCheckbox);
                        // Unched tracing checkbox
                        expect(checkedCheckbox).not.toBeChecked();
                        // Click on 'Add condition'
                        reactTestingLibrary_1.fireEvent.click(modal.getByText('Add Condition'));
                        // Autocomplete
                        const autoCompleteList = yield reactTestingLibrary_1.screen.findByTestId('autocomplete-list');
                        expect(autoCompleteList).toBeInTheDocument();
                        // Condition Options
                        const conditionOptions = modal.queryAllByRole('presentation');
                        // Click on the seventh condition option
                        reactTestingLibrary_1.fireEvent.click(conditionOptions[6]);
                        // Legacy Browsers
                        expect(modal.getByText('All browsers')).toBeTruthy();
                        const legacyBrowsers = Object.keys(utils_2.LEGACY_BROWSER_LIST);
                        for (const legacyBrowser of legacyBrowsers) {
                            const { icon, title } = utils_2.LEGACY_BROWSER_LIST[legacyBrowser];
                            expect(modal.getByText(title)).toBeTruthy();
                            expect(modal.queryAllByTestId(`icon-${icon}`)).toBeTruthy();
                        }
                        expect(modal.queryAllByTestId('icon-internet-explorer')).toHaveLength(4);
                        expect(modal.queryAllByTestId('icon-opera')).toHaveLength(2);
                        expect(modal.queryAllByTestId('icon-safari')).toHaveLength(1);
                        expect(modal.queryAllByTestId('icon-android')).toHaveLength(1);
                        const switchButtons = modal.queryAllByTestId('switch');
                        expect(switchButtons).toHaveLength(legacyBrowsers.length + 1);
                        // All browsers are unchecked
                        for (const switchButton of switchButtons) {
                            expect(switchButton).not.toBeChecked();
                        }
                        // Click on the switch of 'All browsers' option
                        reactTestingLibrary_1.fireEvent.click(switchButtons[0]);
                        // All browsers are now checked
                        for (const switchButton of switchButtons) {
                            expect(switchButton).toBeChecked();
                        }
                        // Button is still disabled
                        const saveRuleButton = modal.getByRole('button', { name: 'Save Rule' });
                        expect(saveRuleButton).toBeTruthy();
                        expect(saveRuleButton).toBeDisabled();
                        // Fill sample rate field
                        const sampleRateField = modal.getByPlaceholderText('\u0025');
                        expect(sampleRateField).toBeTruthy();
                        reactTestingLibrary_1.fireEvent.change(sampleRateField, { target: { value: 20 } });
                        // Save button is now enabled
                        const saveRuleButtonEnabled = modal.getByRole('button', { name: 'Save Rule' });
                        expect(saveRuleButtonEnabled).toBeEnabled();
                        // Click on save button
                        reactTestingLibrary_1.fireEvent.click(saveRuleButtonEnabled);
                        // Modal will close
                        yield (0, reactTestingLibrary_1.waitForElementToBeRemoved)(() => reactTestingLibrary_1.screen.getByText('Add Transaction Sampling Rule'));
                        // Transaction rules panel is updated
                        expect(reactTestingLibrary_1.screen.queryByText('There are no transaction rules to display')).toBeFalsy();
                        const individualTransactionRules = reactTestingLibrary_1.screen.queryAllByText('Individual transactions');
                        expect(individualTransactionRules).toHaveLength(1);
                        expect(reactTestingLibrary_1.screen.getByText('Legacy Browser')).toBeTruthy();
                        for (const legacyBrowser of legacyBrowsers) {
                            const { title } = utils_2.LEGACY_BROWSER_LIST[legacyBrowser];
                            expect(reactTestingLibrary_1.screen.getByText(title)).toBeTruthy();
                        }
                        expect(reactTestingLibrary_1.screen.getByText('20%')).toBeTruthy();
                    });
                });
            });
        });
    });
});
//# sourceMappingURL=projectFiltersAndSampling.spec.jsx.map