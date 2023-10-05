import BackButton from 'components/BackButton'
import { ButtonPrimary } from 'components/Button/Button'
import ComponentsWrapper from 'components/ComponentsWrapper/ComponentsWrapper'
import { StyledButtonWrapper, StyledFormWrapper } from 'pages/Agents/AgentForm/CreateAgentForm'
import {
  StyledHeaderGroup,
  StyledSectionDescription,
  StyledSectionTitle,
  StyledSectionWrapper,
} from 'pages/Home/homeStyle.css'

import Button from '@l3-lib/ui-core/dist/Button'
import Loader from '@l3-lib/ui-core/dist/Loader'
import Textarea from '@l3-lib/ui-core/dist/Textarea'
import Typography from '@l3-lib/ui-core/dist/Typography'

import { FormikProvider } from 'formik'

import FormikTextField from 'components/TextFieldFormik'
import {
  StyledForm,
  StyledInputWrapper,
  StyledRoot,
  StyledTextareaWrapper,
} from 'pages/Agents/AgentForm/AgentForm'
import TypographyPrimary from 'components/Typography/Primary'
import { useCreateContact } from '../useCreateContract'

const CreateContactForm = () => {
  const { formik, isLoading } = useCreateContact()

  const { values, setFieldValue } = formik
  const { contact_description } = values

  const onDescriptionChange = (value: string) => {
    setFieldValue('contact_description', value)
  }

  return (
    <FormikProvider value={formik}>
      <StyledSectionWrapper>
        <StyledHeaderGroup className='header_group'>
          <div>
            <StyledSectionTitle>Add Contact</StyledSectionTitle>
            {/* <StyledSectionDescription>
        Here is your datasource, a collection of databases, APIs, files, and more.
      </StyledSectionDescription> */}
          </div>

          <StyledButtonWrapper>
            <BackButton />
            <ButtonPrimary
              onClick={formik?.handleSubmit}
              size={Button.sizes.SMALL}
              disabled={isLoading}
            >
              {isLoading ? <Loader size={32} /> : 'Save'}
            </ButtonPrimary>
          </StyledButtonWrapper>
        </StyledHeaderGroup>

        <ComponentsWrapper noPadding>
          <StyledFormWrapper>
            <StyledRoot>
              <StyledForm>
                <StyledInputWrapper>
                  <FormikTextField name='contact_name' placeholder='Name' label='Name' />

                  <StyledTextareaWrapper>
                    <TypographyPrimary
                      value='Description'
                      type={Typography.types.LABEL}
                      size={Typography.sizes.md}
                    />
                    <Textarea
                      hint=''
                      placeholder='Description'
                      name='contact_description'
                      value={contact_description}
                      onChange={onDescriptionChange}
                    />

                    <FormikTextField name='contact_phone' placeholder='Phone' label='Phone' />
                    <FormikTextField name='contact_email' placeholder='Email' label='Email' />
                  </StyledTextareaWrapper>
                </StyledInputWrapper>
              </StyledForm>
            </StyledRoot>
          </StyledFormWrapper>
        </ComponentsWrapper>
      </StyledSectionWrapper>
    </FormikProvider>
  )
}

export default CreateContactForm
