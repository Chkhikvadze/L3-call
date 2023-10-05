import TypographyPrimary from 'components/Typography/Primary'
import TypographySecondary from 'components/Typography/Secondary'
import MemberText from 'modals/AIChatModal/components/ChatMembers/components/MemberText'

import styled from 'styled-components'

import IconButton from '@l3-lib/ui-core/dist/IconButton'
import Typography from '@l3-lib/ui-core/dist/Typography'
import { StyledDeleteIcon } from 'pages/TeamOfAgents/TeamOfAgentsCard/TeamOfAgentsCard'

const TempCard = ({
  name,
  description,
  onDeleteClick,
}: {
  name: string
  description: string
  onDeleteClick?: () => void
}) => {
  return (
    <StyledCard>
      {/* <MemberText name={name} role={description} /> */}

      <TypographyPrimary value={name} size={Typography.sizes.lg} />
      <TypographySecondary value={description} size={Typography.sizes.md} />

      <StyledButtonsWrapper className='hiddenButtons'>
        {onDeleteClick && (
          <IconButton
            onClick={onDeleteClick}
            icon={() => <StyledDeleteIcon />}
            size={IconButton.sizes.SMALL}
            kind={IconButton.kinds.TERTIARY}
            // ariaLabel='Delete'
          />
        )}
      </StyledButtonsWrapper>
    </StyledCard>
  )
}

export default TempCard

const StyledCard = styled.div`
  position: relative;

  width: 200px;
  min-width: 200px;
  height: 100px;
  min-height: 100px;

  padding: 0px 20px;

  background: ${({ theme }) => theme.body.cardBgColor};
  border: ${({ theme }) => theme.body.border};
  border-radius: 8px;

  display: flex;
  flex-direction: column;

  justify-content: center;

  :hover {
    .hiddenButtons {
      opacity: 1;
    }
  }
`
const StyledButtonsWrapper = styled.div`
  position: absolute;
  right: 5px;

  opacity: 0;
`
