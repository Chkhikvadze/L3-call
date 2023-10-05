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

import { useCreateGroup } from '../useCreateGroup'
import { FormikProvider } from 'formik'

import FormikTextField from 'components/TextFieldFormik'
import {
  StyledForm,
  StyledInputWrapper,
  StyledTextareaWrapper,
} from 'pages/Agents/AgentForm/AgentForm'
import TypographyPrimary from 'components/Typography/Primary'

const CreateGroupForm = () => {
  const { formik, isLoading } = useCreateGroup()

  const { values, setFieldValue } = formik
  const { group_description } = values

  const onDescriptionChange = (value: string) => {
    setFieldValue('group_description', value)
  }

  return (
    <FormikProvider value={formik}>
      <StyledSectionWrapper>
        <StyledHeaderGroup className='header_group'>
          <div>
            <StyledSectionTitle>Add Group</StyledSectionTitle>
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
          <StyledForm>
            <StyledInputWrapper>
              <FormikTextField name='group_name' placeholder='Name' label='Name' />

              <StyledTextareaWrapper>
                <TypographyPrimary
                  value='Description'
                  type={Typography.types.LABEL}
                  size={Typography.sizes.md}
                />
                <Textarea
                  hint=''
                  placeholder='Description'
                  name='group_description'
                  value={group_description}
                  onChange={onDescriptionChange}
                />
              </StyledTextareaWrapper>
            </StyledInputWrapper>
          </StyledForm>
        </ComponentsWrapper>
      </StyledSectionWrapper>
    </FormikProvider>
  )
}

export default CreateGroupForm
